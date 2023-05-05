import time
from typing import List
import pyautogui
from otsourcing.data_model.extra_action import ExtraAction
from otsourcing.gui.window_utils import only_if_window_focused
from otsourcing.data_model.attack_rotation import AttackRotation


class AttackService:
    def __init__(
        self, attack_rotation: AttackRotation, extra_actions: List[ExtraAction] = None
    ):
        self.timer = time.perf_counter()
        self.attack_rotation = attack_rotation
        self.extra_actions = extra_actions

    @only_if_window_focused
    def attack(self):
        if not self.attack_rotation.is_group_available():
            return False
        attack_spell = self.attack_rotation.get_next_attack()
        if attack_spell:
            if attack_spell.extra_action_hotkey_pre:
                pyautogui.press(attack_spell.extra_action_hotkey_pre)
            pyautogui.press(attack_spell.hotkey)
            self.attack_rotation.reset_last_time_used(attack_spell)
            return True
        return False

    @only_if_window_focused
    def extra_action(self):
        if not self.extra_actions:
            return False
        for extra_action in self.extra_actions:
            if extra_action.is_action_available():
                pyautogui.press(extra_action.hotkey)
                extra_action.reset_last_time_used()
