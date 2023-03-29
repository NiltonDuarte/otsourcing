import pyautogui
from pynput import keyboard
from queue import Queue, Full

from otsourcing.data_model.game_screen_position import GameScreenPosition
from otsourcing.gui.window_utils import only_if_window_focused
from otsourcing.logger import logger


class HotkeyFunctions:
    surrouding_sqms = {
        'north': GameScreenPosition(907, 420),
        'north-left': GameScreenPosition(832, 420),
        'left': GameScreenPosition(832, 497),
        'south-left': GameScreenPosition(832, 574),
        'south': GameScreenPosition(905, 574),
        'south-right': GameScreenPosition(984, 574),
        'right': GameScreenPosition(984, 497),
        'north-right': GameScreenPosition(984, 420),
    }

    @staticmethod
    @only_if_window_focused
    def pickup_surrouding_loot(pago_macro: 'PagoMacro'):
        if pago_macro.paused:
            return
        with pyautogui.hold('shift'):
            for position in HotkeyFunctions.surrouding_sqms.values():
                pyautogui.rightClick(
                    position.get_x_rand_coord(), position.get_y_rand_coord(), interval=0.01)

    @staticmethod
    def pause(pago_macro: 'PagoMacro'):
        pago_macro.toggle_pause()

    @staticmethod
    def toggle_atk(pago_macro: 'PagoMacro'):
        if pago_macro.paused:
            return
        pago_macro.toggle_atk()


class Hotkeys:

    def __init__(self, command_queue: Queue) -> None:
        self.command_queue = command_queue
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

    def send_to_command_queue(self, key):
        try:
            self.command_queue.put_nowait(key)
        except Full:
            logger.error("Queue is full")

    def on_press(self, key: keyboard.KeyCode or keyboard.Key):
        if key == keyboard.Key.pause:
            self.send_to_command_queue(key)
            return
        if not isinstance(key, keyboard.KeyCode):
            return
        if key.char in ('r', 'd'):
            self.send_to_command_queue(key)

    def on_release(self, key):
        ...

    def run(self):
        self.listener.start()
