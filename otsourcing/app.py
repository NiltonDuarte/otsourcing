from otsourcing.apps.healing_app import HealingApp
from otsourcing.apps.attack_app import AttackApp
from otsourcing.apps.cavebot_app import CavebotApp


class OtSorcing:
    def __init__(self) -> None:
        self.healing_app = HealingApp
        self.attack_app = AttackApp
        self.cavebot_app = CavebotApp
