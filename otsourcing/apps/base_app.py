from queue import Queue, Empty, Full
from pynput import keyboard
from otsourcing.data_model.command_message import (
    StringMessage,
    TogglePauseMessage,
)
import pyautogui
from otsourcing.services.hotkeys import HotkeyFunctions
from otsourcing.logger import logger


class BaseApp:
    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        self.name = name
        self.input_command_queue = input_command_queue
        self.output_command_queue = output_command_queue
        self.resumed = False
        self.log = logger
        pyautogui.FAILSAFE = False

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
            self.log.error("Output queue full")

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
