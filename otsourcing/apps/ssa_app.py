import pyautogui
import yaml
from otsourcing.logger import logger
from otsourcing.data_model.amulet import Amulet
from otsourcing.services.ssa import SsaService
from otsourcing.settings import user_resources_folder
from otsourcing.apps.base_app import BaseApp


class SsaApp(BaseApp):
    def __init__(self, *args, **kwargs):
        self.ssa_service = None
        self.toggle_hotkey = None
        super().__init__(*args, **kwargs)

    def load_config_from_file(self, ssa_file_name):
        with open(f"{user_resources_folder}/ssa/{ssa_file_name}.yaml") as f:
            user_input = yaml.safe_load(f)
        ssa_config = user_input["ssa_config"]
        self.send_output(f"Loading config {ssa_config['name']}")
        self.toggle_hotkey = ssa_config["toggle_hotkey"]
        amulet = Amulet.load_from_dict(ssa_config["amulet"])

        self.ssa_service = SsaService(amulet=amulet, **ssa_config["ssa_service"])

    def queue_handler(self):
        hotkey_map = {
            self.toggle_hotkey: self.toggle_ssa,
        }
        super()._queue_handler(hotkey_map)

    def toggle_ssa(self):
        self.ssa_service.ssa_enable = not self.ssa_service.ssa_enable
        self.send_output(f"SSA = {self.ssa_service.ssa_enable}")

    def run(self):
        self.send_output("Initializing ssa.")

        while True:
            self.queue_handler()
            if not self.resumed:
                logger.debug(f"{self.name} paused.")
                pyautogui.sleep(1)
                continue

            has_equipped, message = self.ssa_service.handle_ssa() or (False, None)
            if has_equipped and message:
                self.send_output(message)
            pyautogui.sleep(0.05)
