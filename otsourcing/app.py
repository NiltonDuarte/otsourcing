import pyautogui
from pynput import keyboard
from dataclasses import dataclass
from queue import Queue, Empty, Full
from otsourcing.services.cavebot.cavebot import CavebotService

from otsourcing.services.hotkeys import HotkeyFunctions
from otsourcing.logger import logger
from otsourcing.services.heal import HealService
from otsourcing.services.mana import ManaService
from otsourcing.services.attack import AttackService
from cavebot.waypoints.three_marks import marks_used


class BaseApp:
    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        self.name = name
        self.input_command_queue = input_command_queue
        self.output_command_queue = output_command_queue
        self.paused = True

    def toggle_pause(self):
        self.paused = not self.paused
        self.send_output(f"Pause={self.paused}")

    def send_output(self, message):
        fmt_message = f"{self.name}: {message}"
        try:
            self.output_command_queue.put_nowait(fmt_message)
        except Full:
            logger.error("Output queue full")

    def _queue_handler(self, hotkey_map):
        try:
            while not self.input_command_queue.empty():
                key = self.input_command_queue.get_nowait()
                if key == keyboard.Key.pause:
                    HotkeyFunctions.pause(self)
                    continue
                if self.paused:
                    continue
                if isinstance(key, keyboard.KeyCode):
                    fn = hotkey_map.get(key.char)
                else:
                    fn = hotkey_map.get(key)
                if fn is not None:
                    fn()
        except Empty:
            ...


class HealingApp(BaseApp):

    def queue_handler(self):
        hotkey_map = {
            'r': lambda: HotkeyFunctions.pickup_surrouding_loot(self),
            's': self.toggle_ssa,
        }
        super()._queue_handler(hotkey_map)

    def toggle_ssa(self):
        self.health_service.ssa_enable = not self.health_service.ssa_enable
        self.send_output(f"SSA = {self.health_service.ssa_enable}")

    def run(self):
        self.send_output("Setting up healing.")
        self.health_service = HealService()
        self.mana_service = ManaService()
        self.send_output("Initializing healing.")

        while True:
            self.queue_handler()
            if self.paused:
                pyautogui.sleep(1)
                continue

            has_healed, message = self.health_service.heal() or (False, None)
            if has_healed and message:
                self.send_output(message)
            has_filled, message = self.mana_service.fill() or (False, None)
            if has_filled and message:
                self.send_output(message)
            pyautogui.sleep(0.1)


class AttackApp(BaseApp):

    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        super().__init__(name, input_command_queue, output_command_queue)
        self.atk_enabled = False

    def toggle_atk(self):
        self.atk_enabled = not self.atk_enabled
        self.send_output(f"Atk Enabled={self.atk_enabled}")

    def queue_handler(self):
        hotkey_map = {
            'd': lambda: HotkeyFunctions.toggle_atk(self),
        }
        super()._queue_handler(hotkey_map)

    def run(self):
        self.send_output("Setting up attack.")
        attack_service = AttackService()
        self.send_output("Initializing attack.")
        while True:
            self.queue_handler()
            if self.paused:
                pyautogui.sleep(1)
                continue
            if self.atk_enabled:
                attack_service.attack()
            else:
                pyautogui.sleep(1)


class CavebotApp(BaseApp):

    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        super().__init__(name, input_command_queue, output_command_queue)
        self.marks = marks_used

    def queue_handler(self):
        hotkey_map = {
        }
        super()._queue_handler(hotkey_map)

    def wait_if_paused(self):
        while True:
            self.queue_handler()
            if not self.paused:
                return
            pyautogui.sleep(1)

    def set_cavebot(self, marks):
        self.marks = marks

    def run(self):
        self.send_output("Setting up macro cavebot.")
        cavebot_service = CavebotService()
        self.send_output("Initializing cavebot.")
        while True:
            for mark in self.marks:
                self.wait_if_paused()
                self.send_output(f"Doing mark {mark.name}.")
                cavebot_service.do_mark(mark)


class OtSorcing:
    def __init__(self) -> None:
        self.healing_app = HealingApp
        self.attack_app = AttackApp
        self.cavebot_app = CavebotApp
