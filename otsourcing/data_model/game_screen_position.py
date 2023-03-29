from dataclasses import dataclass
import random


@dataclass
class GameScreenPosition:
    x_coord: int
    y_coord: int
    x_var: int = 20
    y_var: int = 20

    def get_x_rand_coord(self):
        return self.x_coord + random.randint(-self.x_var, self.x_var)

    def get_y_rand_coord(self):
        return self.y_coord + random.randint(-self.y_var, self.y_var)
