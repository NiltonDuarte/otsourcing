import pyautogui
import pyscreeze
import time
from pyscreeze import RGB
from otsourcing.data_model.health import HealthBar
from otsourcing.data_model.amulet import Amulet
from otsourcing.gui.window_utils import only_if_window_focused, is_gray


class HealService:
    health_bar = HealthBar()
    amulet = Amulet()
    spell_heal_key = 'f1'
    pot_heal_key = 'f2'
    is_full_ssa = False
    ssa_enable = False
    ssa_equiped = False
    heal_cd = 1
    ssa_cd = 0.2

    def __init__(self):
        self.ssa_timer = time.perf_counter()
        self.spell_timer = time.perf_counter()

    @only_if_window_focused
    def heal(self):
        health_bar_pot_color = RGB(
            *pyscreeze.pixel(self.health_bar.pot_x, self.health_bar.y))
        if is_gray(health_bar_pot_color):
            pyautogui.press(self.pot_heal_key)
            self.spell_heal()
            self.equip_ssa()
            return True, "Pot and Spell heal"

        health_bar_ssa_color = RGB(
            *pyscreeze.pixel(self.health_bar.ssa_x, self.health_bar.y))
        if self.is_full_ssa:
            self.equip_ssa()
        elif is_gray(health_bar_ssa_color) and self.ssa_enable:
            self.spell_heal()
            self.equip_ssa()
        else:
            self.equip_default_amulet()

        health_bar_spell_color = RGB(
            *pyscreeze.pixel(self.health_bar.spell_x, self.health_bar.y))
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
        amulet_slot_color = RGB(
            *pyscreeze.pixel(self.amulet.x, self.amulet.y))
        if amulet_slot_color != self.amulet.ssa_pixel:
            pyautogui.press(self.amulet.ssa_hotkey)
            self.ssa_timer = time.perf_counter()
            self.ssa_equiped = True

    def equip_default_amulet(self):
        amulet_slot_color = RGB(
            *pyscreeze.pixel(self.amulet.x, self.amulet.y))
        if self.ssa_equiped and amulet_slot_color != self.amulet.ssa_pixel:
            pyautogui.press(self.amulet.default_amulet_hotkey)
            self.ssa_equiped = False
