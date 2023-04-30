import time
import pyautogui
import pyscreeze
from pyscreeze import RGB
from otsourcing.data_model.health import HealthBar
from otsourcing.data_model.amulet import Amulet
from otsourcing.gui.window_utils import only_if_window_focused, is_gray


class HealService:
    def __init__(
        self,
        spell_heal_key,
        pot_heal_key,
        heal_cd,
        health_bar: HealthBar,
    ):
        self.spell_heal_key = spell_heal_key
        self.pot_heal_key = pot_heal_key
        self.heal_cd = heal_cd
        self.health_bar = health_bar

        self.spell_timer = time.perf_counter()

    @only_if_window_focused
    def heal(self):
        health_bar_pot_color = RGB(
            *pyscreeze.pixel(self.health_bar.pot_x, self.health_bar.y)
        )
        if is_gray(health_bar_pot_color):
            pyautogui.press(self.pot_heal_key)
            self.spell_heal()
            return True, "Pot and Spell heal"

        health_bar_spell_color = RGB(
            *pyscreeze.pixel(self.health_bar.spell_x, self.health_bar.y)
        )
        if is_gray(health_bar_spell_color):
            self.spell_heal()
            return True, ""
        return False, "Life not healed"

    def spell_heal(self):
        current_timer = time.perf_counter()
        diff = current_timer - self.spell_timer
        if diff > self.heal_cd:
            pyautogui.press(self.spell_heal_key)
            self.spell_timer = time.perf_counter()
