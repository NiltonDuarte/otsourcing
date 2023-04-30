from dataclasses import dataclass
from typing import Tuple
from pyscreeze import RGB


@dataclass
class Amulet:
    ssa_pixel_pos: Tuple[int, int]
    ssa_pixel_color: RGB
    ssa_pixel_health_pos: Tuple[int, int]

    @classmethod
    def load_from_dict(cls, input_dict):
        input_dict["ssa_pixel_color"] = RGB(*input_dict["ssa_pixel_color"])
        return cls(**input_dict)
