import pyautogui
import pyscreeze
from pyscreeze import RGB
from otsourcing.data_model.health import HealthBar
from otsourcing.data_model.amulet import Amulet
from otsourcing.gui.window_utils import only_if_window_focused, is_gray


class HealService:
    health_bar = HealthBar()
    amulet = Amulet()
    spell_heal_key = 'f1'
    pot_heal_key = 'f2'
    is_full_ssa = True
    ssa_enable = False
    ssa_equiped = False

    @only_if_window_focused
    def heal(self):
        health_bar_pot_color = RGB(
            *pyscreeze.pixel(self.health_bar.pot_x, self.health_bar.y))
        if is_gray(health_bar_pot_color):
            pyautogui.press(self.pot_heal_key)
            pyautogui.press(self.spell_heal_key)
            self.equip_ssa()
            return True, "Pot and Spell heal"

        health_bar_ssa_color = RGB(
            *pyscreeze.pixel(self.health_bar.ssa_x, self.health_bar.y))
        if self.is_full_ssa:
            self.equip_ssa()
        elif is_gray(health_bar_ssa_color) and self.ssa_enable:
            pyautogui.press(self.spell_heal_key)
            self.equip_ssa()
            return True, "SSA Up"
        else:
            self.equip_default_amulet()
        health_bar_spell_color = RGB(
            *pyscreeze.pixel(self.health_bar.spell_x, self.health_bar.y))
        if is_gray(health_bar_spell_color):
            pyautogui.press(self.spell_heal_key)
            return True, ""
        return False, "Life not healed"

    def equip_ssa(self):
        if not self.ssa_enable:
            return
        amulet_slot_color = RGB(
            *pyscreeze.pixel(self.amulet.x, self.amulet.y))
        if amulet_slot_color != self.amulet.ssa_pixel:
            pyautogui.press(self.amulet.ssa_hotkey)
            self.ssa_equiped = True

    def equip_default_amulet(self):
        amulet_slot_color = RGB(
            *pyscreeze.pixel(self.amulet.x, self.amulet.y))
        if self.ssa_equiped and amulet_slot_color != self.amulet.ssa_pixel:
            pyautogui.press(self.amulet.default_amulet_hotkey)
            self.ssa_equiped = False
