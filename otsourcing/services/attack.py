import time
import random
import pyautogui
from otsourcing.gui.window_utils import only_if_window_focused
from otsourcing.data_model.attack_rotation import SpellRotation
from otsourcing.data_model.attack import AttackSpell


class AttackService:
    def __init__(self, spell_rotation: SpellRotation):
        self.timer = time.perf_counter()
        self.spell_rotation = spell_rotation

    @only_if_window_focused
    def attack(self):
        if not self.spell_rotation.is_group_available():
            return False
        attack_spell = self.spell_rotation.get_next_spell()
        if attack_spell:
            pyautogui.press(attack_spell.hotkey)
            attack_spell.reset_last_time_used()
            self.spell_rotation.reset_last_time_used()
            return True
        return False
