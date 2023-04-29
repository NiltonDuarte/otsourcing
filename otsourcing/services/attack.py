import time
import pyautogui
from otsourcing.gui.window_utils import only_if_window_focused
from otsourcing.data_model.attack_rotation import AttackRotation


class AttackService:
    def __init__(self, attack_rotation: AttackRotation):
        self.timer = time.perf_counter()
        self.attack_rotation = attack_rotation

    @only_if_window_focused
    def attack(self):
        if not self.attack_rotation.is_group_available():
            return False
        attack_spell = self.attack_rotation.get_next_attack()
        if attack_spell:
            pyautogui.press(attack_spell.hotkey)
            self.attack_rotation.reset_last_time_used(attack_spell)
            return True
        return False
