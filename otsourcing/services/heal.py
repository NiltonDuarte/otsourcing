import pyautogui
import pyscreeze
from pyscreeze import RGB
from otsourcing.data_model.health import HealthBar
from otsourcing.gui.window_utils import only_if_window_focused, is_gray


class HealService:
    health_bar = HealthBar()
    spell_heal_key = 'f1'
    pot_heal_key = 'f2'

    @only_if_window_focused
    def heal(self):
        health_bar_pot_color = RGB(
            *pyscreeze.pixel(self.health_bar.pot_x, self.health_bar.y))
        if is_gray(health_bar_pot_color):
            pyautogui.press(self.pot_heal_key)
            pyautogui.press(self.spell_heal_key)
            return True, "Pot and Spell heal"
        health_bar_spell_color = RGB(
            *pyscreeze.pixel(self.health_bar.spell_x, self.health_bar.y))
        if is_gray(health_bar_spell_color):
            pyautogui.press(self.spell_heal_key)
            return True, ""
        return False, "Life not healed"
