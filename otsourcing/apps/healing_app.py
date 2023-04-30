import pyautogui
import yaml
from otsourcing.data_model.amulet import Amulet
from otsourcing.data_model.attack_rotation import AttackRotation
from otsourcing.data_model.health import HealthBar
from otsourcing.data_model.mana import ManaBar
from otsourcing.services.hotkeys import HotkeyFunctions
from otsourcing.services.heal import HealService
from otsourcing.services.mana import ManaService
from otsourcing.settings import user_resources_folder
from otsourcing.apps.base_app import BaseApp


class HealingApp(BaseApp):
    def __init__(self, *args, **kwargs):
        self.health_service = None
        self.mana_service = None
        super().__init__(*args, **kwargs)

    def load_config_from_file(self, healing_file_name):
        with open(f"{user_resources_folder}/heal/{healing_file_name}.yaml") as f:
            user_input = yaml.safe_load(f)
        heal_config = user_input["heal_config"]
        self.send_output(f"Loading config {heal_config['name']}")
        health_bar = HealthBar.load_from_dict(heal_config["health_bar"])
        mana_bar = ManaBar.load_from_dict(heal_config["mana_bar"])

        self.health_service = HealService(
            health_bar=health_bar, **heal_config["heal_service"]
        )
        self.mana_service = ManaService(
            mana_bar=mana_bar, **heal_config["mana_service"]
        )

    def queue_handler(self):
        hotkey_map = {
            "r": lambda: HotkeyFunctions.pickup_surrouding_loot(self),
        }
        super()._queue_handler(hotkey_map)

    def run(self):
        self.send_output("Initializing healing.")

        while True:
            self.queue_handler()
            if not self.resumed:
                pyautogui.sleep(1)
                continue

            has_healed, message = self.health_service.heal() or (False, None)
            if has_healed and message:
                self.send_output(message)
            has_filled, message = self.mana_service.fill() or (False, None)
            if has_filled and message:
                self.send_output(message)
            pyautogui.sleep(0.05)
