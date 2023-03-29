import time
import random
import pyautogui


class AttackService:
    spell_hk = '6'
    rune_hk = '8'
    spell_rotation_map = {
        'spell': {'hk': 'f4', 'next': 'rune'},
        'rune': {'hk': 'f5', 'next': 'spell'},
    }

    def __init__(self):
        self.timer = time.perf_counter()
        self.next_atk = 'spell'

    def attack(self):
        current_timer = time.perf_counter()
        diff = current_timer - self.timer
        if diff > (2 + random.random()/5):
            spell_rotation = self.spell_rotation_map[self.next_atk]
            pyautogui.press(spell_rotation['hk'])
            self.next_atk = spell_rotation['next']
            self.timer = time.perf_counter()
