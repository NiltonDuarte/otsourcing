from dataclasses import dataclass


@dataclass
class ManaBar:
    y: int
    pot_x: int
    high_mana_pot_x: int

    @classmethod
    def load_from_dict(cls, input_dict):
        return cls(**input_dict)
