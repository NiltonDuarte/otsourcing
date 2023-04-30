from dataclasses import dataclass
from pyscreeze import RGB


@dataclass
class Amulet:
    x: int
    y: int
    ssa_pixel: int

    @classmethod
    def load_from_dict(cls, input_dict):
        input_dict["ssa_pixel"] = RGB(*input_dict["ssa_pixel"])
        return cls(**input_dict)
