from queue import Queue
import pyautogui
import yaml
from otsourcing.data_model.attack_rotation import AttackRotation
from otsourcing.data_model.command_message import (
    ToggleAtkMessage,
)
from otsourcing.data_model.extra_action import ExtraAction
from otsourcing.services.battle import BattleService
from otsourcing.services.hotkeys import HotkeyFunctions
from otsourcing.services.attack import AttackService
from otsourcing.settings import user_resources_folder
from otsourcing.apps.base_app import BaseApp


class AttackApp(BaseApp):
    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        super().__init__(name, input_command_queue, output_command_queue)
        self.atk_enabled = False
        self.attack_rotation = None

    def load_config_from_file(self, attack_file_name):
        with open(f"{user_resources_folder}/attack/{attack_file_name}.yaml") as f:
            user_input = yaml.safe_load(f)
        attack_config = user_input["attack_config"]
        self.send_output(f"Loading config {attack_config['name']}")
        attack_rotation = AttackRotation.load_from_dict(
            attack_config["attack_rotation"]
        )
        extra_actions = []
        for extra_action_input in attack_config.get("extra_actions", []):
            extra_action = ExtraAction.load_from_dict(extra_action_input["action"])
            extra_actions.append(extra_action)
        self.attack_service = AttackService(attack_rotation, extra_actions)

    def toggle_atk(self):
        self.atk_enabled = not self.atk_enabled
        cmd = ToggleAtkMessage(self.name, self.atk_enabled)
        self.send_output(cmd)

    def queue_handler(self):
        hotkey_map = {
            "d": lambda: HotkeyFunctions.toggle_atk(self),
        }
        super()._queue_handler(hotkey_map)

    def run(self):
        self.send_output("Initializing attack.")
        while True:
            self.queue_handler()
            if not self.resumed:
                pyautogui.sleep(1)
                continue
            if not self.atk_enabled:
                pyautogui.sleep(1)
                continue
            if BattleService.is_battle_empty():
                pyautogui.sleep(1)
                continue
            has_attacked = self.attack_service.attack()
            self.attack_service.extra_action()
            pyautogui.sleep(0.1)
