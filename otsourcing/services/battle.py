import pyscreeze
from pyscreeze import RGB
from otsourcing.settings import life_border_pos


class BattleService:
    not_empty_color = RGB(0, 0, 0)

    @classmethod
    def is_battle_empty(cls):
        battle_color = RGB(*pyscreeze.pixel(*life_border_pos))
        if (
            battle_color.red != cls.not_empty_color.red
            or battle_color.green != cls.not_empty_color.green
            or battle_color.blue != cls.not_empty_color.blue
        ):
            return True
        return False
