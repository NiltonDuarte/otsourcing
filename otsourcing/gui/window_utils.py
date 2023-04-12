import pyautogui
import time
from pyscreeze import RGB
from otsourcing.logger import logger
from otsourcing.settings import WINDOW_TITLE_IMG


def is_gray(color: RGB, tolerance=10):
    # print(color)
    return (abs(color.red - color.green) < tolerance) and (abs(color.green - color.blue) < tolerance)


def is_window_active():
    window_title = (70, 0, 190-70, 20)
    pos = pyautogui.locateCenterOnScreen(
        WINDOW_TITLE_IMG,
        region=window_title,
        minSearchTime=0)
    if not pos:
        logger.debug("Waiting window focus")
        pyautogui.sleep(0.5)
        return False
    return True


def only_if_window_focused(func):
    def wrapper(*args, **kwargs):
        if is_window_active():
            return func(*args, **kwargs)
    return wrapper


@only_if_window_focused
def locateCenterOnScreen(*args, **kwargs):
    pyautogui.press('esc')
    time.sleep(0.15)
    return pyautogui.locateCenterOnScreen(*args, **kwargs)


def click(pos_x, pos_y):
    pyautogui.moveTo(pos_x, pos_y)
    time.sleep(0.1)
    pyautogui.click(pos_x, pos_y)
