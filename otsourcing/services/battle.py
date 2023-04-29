import pyscreeze
from pyscreeze import RGB


class BattleServisce:
    life_border_x = 1594
    life_border_y = 55
    not_empty_color = RGB(0, 0, 0)

    @classmethod
    def is_battle_empty(cls):
        battle_color = RGB(*pyscreeze.pixel(cls.life_border_x, cls.life_border_y))
        if (
            battle_color.red != cls.not_empty_color.red
            or battle_color.green != cls.not_empty_color.green
            or battle_color.blue != cls.not_empty_color.blue
        ):
            return True
        return False
