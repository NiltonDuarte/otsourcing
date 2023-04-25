import pyautogui
import yaml
from pynput import keyboard
from dataclasses import dataclass
from queue import Queue, Empty, Full
from otsourcing.data_model.attack_rotation import SpellRotation
from otsourcing.data_model.command_message import StringMessage, ToggleAtkMessage, TogglePauseMessage
from otsourcing.services.battle import BattleServisce
from otsourcing.services.cavebot.cavebot import CavebotService

from otsourcing.services.hotkeys import HotkeyFunctions
from otsourcing.logger import logger
from otsourcing.services.heal import HealService
from otsourcing.services.mana import ManaService
from otsourcing.services.attack import AttackService
from otsourcing.settings import user_resources_folder
from cavebot.waypoints.three_marks import marks_used


class BaseApp:
    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        self.name = name
        self.input_command_queue = input_command_queue
        self.output_command_queue = output_command_queue
        self.resumed = False

    def toggle_pause(self):
        self.resumed = not self.resumed
        cmd = TogglePauseMessage(self.name, self.resumed)
        self.send_output(cmd)

    def send_output(self, cmd):
        if isinstance(cmd, str):
            cmd = StringMessage(self.name, message=cmd)
        try:
            self.output_command_queue.put_nowait(cmd)
        except Full:
            logger.error("Output queue full")

    def _queue_handler(self, hotkey_map):
        try:
            while not self.input_command_queue.empty():
                key = self.input_command_queue.get_nowait()
                if key == keyboard.Key.pause:
                    HotkeyFunctions.pause(self)
                    continue
                if not self.resumed:
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
            if not self.resumed:
                pyautogui.sleep(1)
                continue

            has_healed, message = self.health_service.heal() or (False, None)
            if has_healed and message:
                self.send_output(message)
            has_filled, message = self.mana_service.fill() or (False, None)
            if has_filled and message:
                self.send_output(message)
            pyautogui.sleep(0.05)


class AttackApp(BaseApp):

    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        super().__init__(name, input_command_queue, output_command_queue)
        self.atk_enabled = False

    def toggle_atk(self):
        self.atk_enabled = not self.atk_enabled
        cmd = ToggleAtkMessage(self.name, self.atk_enabled)
        self.send_output(cmd)

    def queue_handler(self):
        hotkey_map = {
            'd': lambda: HotkeyFunctions.toggle_atk(self),
        }
        super()._queue_handler(hotkey_map)

    def run(self):
        with open(f"{user_resources_folder}/attack/default.yaml") as f:
            user_input = yaml.safe_load(f)
        spell_rotation = SpellRotation.load_from_dict(
            user_input["spell_rotation"])
        self.send_output("Setting up attack.")
        attack_service = AttackService(spell_rotation)
        self.send_output("Initializing attack.")
        while True:
            self.queue_handler()
            if not self.resumed:
                pyautogui.sleep(1)
                continue
            if not self.atk_enabled:
                pyautogui.sleep(1)
                continue
            if BattleServisce.is_battle_empty():
                pyautogui.sleep(1)
                continue
            has_attacked = attack_service.attack()
            pyautogui.sleep(0.1)


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
            if self.resumed:
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
