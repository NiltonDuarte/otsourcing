import time
from random import random
import pyautogui
from pyscreeze import RGB

from otsourcing.data_model.map_mark import Mark
from otsourcing.settings import creature_icon_pos
from otsourcing.gui.window_utils import is_gray


def wait_to_empty_battle(mark: Mark):
    if not mark.check_battle:
        return
    print("entering wait_to_empty_battle")
    time.sleep(0.2 + random())
    creature_pixel_color = RGB(*pyautogui.pixel(*creature_icon_pos))

    num_cycles = 0
    print(f"{creature_pixel_color=}")
    while not is_gray(creature_pixel_color):
        yield None
        num_cycles += 1
        time.sleep(0.1 + random() / 2)
        if num_cycles > 400:
            pyautogui.screenshot("battle_stuck.png")
            raise RuntimeError("Stopping macro due to something stuck on battle")
        creature_pixel_color = RGB(*pyautogui.pixel(*creature_icon_pos))

    print("exiting wait_to_empty_battle")
