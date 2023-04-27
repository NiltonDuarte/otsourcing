import time
from typing import List
from dataclasses import dataclass
from otsourcing.data_model.attack import AttackSpell


@dataclass
class AttackRotation:
    rotation: List[AttackSpell]
    group_cooldown: int = 2
    last_time_used: int = 0

    def reset_last_time_used(self, attack_spell: AttackSpell):
        attack_spell.reset_last_time_used()
        self.last_time_used = time.perf_counter()

    def is_group_available(self):
        current_timer = time.perf_counter()
        diff = current_timer - self.last_time_used
        if diff > self.group_cooldown:
            return True
        return False

    def get_next_attack(self):
        for attack_spell in self.rotation:
            if attack_spell.is_spell_available():
                return attack_spell

    @classmethod
    def load_from_dict(cls, input_dict):
        rotation = []
        for attack_spell_input in input_dict:
            attack_spell = AttackSpell.load_from_dict(
                attack_spell_input["attack"])
            rotation.append(attack_spell)
        return cls(rotation=rotation)
