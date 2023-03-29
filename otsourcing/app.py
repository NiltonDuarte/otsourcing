import pyautogui
from pynput import keyboard
from dataclasses import dataclass
from queue import Queue, Empty, Full

from otsourcing.services.hotkeys import HotkeyFunctions
from otsourcing.logger import logger
from otsourcing.services.heal import HealService
from otsourcing.services.mana import ManaService
from otsourcing.services.attack import AttackService


class PagoMacro:
    def __init__(self, input_command_queue: Queue, output_command_queue: Queue):
        self.input_command_queue = input_command_queue
        self.output_command_queue = output_command_queue
        self.paused = True
        self.atk_enabled = False

    def toggle_pause(self):
        self.paused = not self.paused
        self.output_command_queue.put(f"Pause={self.paused}")

    def toggle_atk(self):
        self.atk_enabled = not self.atk_enabled
        self.output_command_queue.put(f"Atk Enabled={self.atk_enabled}")

    def queue_handler(self):
        hotkey_map = {
            'r': lambda: HotkeyFunctions.pickup_surrouding_loot(self),
            'd': lambda: HotkeyFunctions.toggle_atk(self),
        }
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

    def send_output(self, message):
        try:
            self.output_command_queue.put_nowait(message)
        except Full:
            logger.error("Output queue full")

    def run(self):
        self.send_output("Setting up Pago Macro.")
        health_service = HealService()
        mana_service = ManaService()
        attack_service = AttackService()
        self.send_output("Initializing macro.")

        while True:
            self.queue_handler()
            if self.paused:
                pyautogui.sleep(1)
                continue

            has_healed, message = health_service.heal() or (False, None)
            if has_healed and message:
                self.send_output(message)
            has_filled, message = mana_service.fill() or (False, None)
            if has_filled:
                self.send_output(message)

            if self.atk_enabled:
                attack_service.attack()
            pyautogui.sleep(0.1)
