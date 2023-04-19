import pyautogui
import pyscreeze
from pyscreeze import RGB

from otsourcing.data_model.mana import ManaBar
from otsourcing.services.battle import BattleServisce
from otsourcing.gui.window_utils import only_if_window_focused, is_gray


class ManaService:
    mana_bar = ManaBar()
    pot_mana_key = 'f3'
    pot_until_high_mana = True

    @only_if_window_focused
    def fill(self):
        mana_bar_color = RGB(
            *pyscreeze.pixel(self.mana_bar.pot_x, self.mana_bar.y)
        )
        if is_gray(mana_bar_color):
            pyautogui.press(self.pot_mana_key)
            return True, "Mana fill"
        elif self.pot_until_high_mana and BattleServisce.is_battle_empty():
            mana_bar_color = RGB(
                *pyscreeze.pixel(self.mana_bar.high_mana_pot_x, self.mana_bar.y)
            )
            if is_gray(mana_bar_color):
                pyautogui.press(self.pot_mana_key)
                return True, None
        return False, "Mana not filled"
