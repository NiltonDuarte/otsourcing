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
        ssa_key,
        default_amulet_key,
        is_full_ssa,
        heal_cd,
        ssa_cd,
        health_bar: HealthBar,
        amulet: Amulet,
    ):
        self.spell_heal_key = spell_heal_key
        self.pot_heal_key = pot_heal_key
        self.ssa_key = ssa_key
        self.default_amulet_key = default_amulet_key
        self.is_full_ssa = is_full_ssa
        self.heal_cd = heal_cd
        self.ssa_cd = ssa_cd
        self.health_bar = health_bar
        self.amulet = amulet

        self.ssa_enable = False
        self.ssa_equiped = False
        self.ssa_timer = time.perf_counter()
        self.spell_timer = time.perf_counter()

    @only_if_window_focused
    def heal(self):
        health_bar_pot_color = RGB(
            *pyscreeze.pixel(self.health_bar.pot_x, self.health_bar.y)
        )
        if is_gray(health_bar_pot_color):
            pyautogui.press(self.pot_heal_key)
            self.spell_heal()
            self.equip_ssa()
            return True, "Pot and Spell heal"

        health_bar_ssa_color = RGB(
            *pyscreeze.pixel(self.health_bar.ssa_x, self.health_bar.y)
        )
        if self.is_full_ssa:
            self.equip_ssa()
        elif is_gray(health_bar_ssa_color) and self.ssa_enable:
            self.spell_heal()
            self.equip_ssa()
        else:
            self.equip_default_amulet()

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

    def equip_ssa(self):
        current_timer = time.perf_counter()
        diff = current_timer - self.ssa_timer
        if not self.ssa_enable:
            return
        if diff < self.ssa_cd:
            return
        amulet_slot_color = RGB(*pyscreeze.pixel(self.amulet.x, self.amulet.y))
        if amulet_slot_color != self.amulet.ssa_pixel:
            pyautogui.press(self.ssa_key)
            self.ssa_timer = time.perf_counter()
            self.ssa_equiped = True

    def equip_default_amulet(self):
        amulet_slot_color = RGB(*pyscreeze.pixel(self.amulet.x, self.amulet.y))
        if self.ssa_equiped and amulet_slot_color != self.amulet.ssa_pixel:
            pyautogui.press(self.default_amulet_key)
            self.ssa_equiped = False
