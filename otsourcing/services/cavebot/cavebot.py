import time

from otsourcing.services.cavebot.battle import wait_to_empty_battle
from otsourcing.services.cavebot.walk import click_on_mark, click_mark_with_retry
import pyautogui


class CavebotService:
    def do_mark(self, mark):
        click_on_mark(mark)
        time.sleep(mark.delay)

        for _ in click_mark_with_retry(mark):
            pyautogui.press("esc")
            pyautogui.press("tab")
            time.sleep(1)
        for _ in wait_to_empty_battle(mark):
            pyautogui.press("esc")
            pyautogui.press("tab")
            time.sleep(1)
        if mark.special_action is not None:
            mark.special_action()
        for _ in wait_to_empty_battle(mark):
            pyautogui.press("esc")
            pyautogui.press("tab")
            time.sleep(1)
