from dataclasses import dataclass


@dataclass
class HealthBar:
    y: int
    pot_x: int
    spell_x: int
    ssa_x: int

    @classmethod
    def load_from_dict(cls, input_dict):
        return cls(**input_dict)
