import time
import random
from dataclasses import dataclass


@dataclass
class AttackSpell:
    hotkey: str
    cooldown: int
    group_cooldown: int = 2
    last_time_used: float = 0
    extra_action_hotkey_pre: str = None

    def is_spell_available(self):
        current_timer = time.perf_counter()
        diff = current_timer - self.last_time_used
        if diff > (self.cooldown + random.random() / 5):
            return True
        return False

    def reset_last_time_used(self):
        self.last_time_used = time.perf_counter()

    @classmethod
    def load_from_dict(cls, input_dict):
        return cls(**input_dict)
