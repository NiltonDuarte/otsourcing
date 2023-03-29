import pyautogui
from pyscreeze import RGB
from otsourcing.logger import logger
from otsourcing.settings import WINDOW_TITLE_IMG


def is_gray(color: RGB, tolerante=10):
    # print(color)
    return (abs(color.red - color.green) < tolerante) and (abs(color.green - color.blue) < tolerante)


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
