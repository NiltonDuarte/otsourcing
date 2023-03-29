import pyautogui
import pyscreeze
from pyscreeze import RGB

from otsourcing.data_model.mana import ManaBar
from otsourcing.gui.window_utils import only_if_window_focused, is_gray


class ManaService:
    mana_bar = ManaBar()
    pot_mana_key = 'f3'

    @only_if_window_focused
    def fill(self):
        mana_bar_color = RGB(
            *pyscreeze.pixel(self.mana_bar.pot_x, self.mana_bar.y)
        )
        if is_gray(mana_bar_color):
            pyautogui.press(self.pot_mana_key)
            return True, "Mana fill"
        return False, "Mana not filled"
