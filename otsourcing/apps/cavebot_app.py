from queue import Queue
import pyautogui
from otsourcing.services.cavebot.cavebot import CavebotService
from otsourcing.apps.base_app import BaseApp
from cavebot.waypoints.three_marks import marks_used


class CavebotApp(BaseApp):
    def __init__(self, name, input_command_queue: Queue, output_command_queue: Queue):
        super().__init__(name, input_command_queue, output_command_queue)
        self.marks = marks_used

    def queue_handler(self):
        hotkey_map = {}
        super()._queue_handler(hotkey_map)

    def wait_if_paused(self):
        while True:
            self.queue_handler()
            if self.resumed:
                return
            pyautogui.sleep(1)

    def set_cavebot(self, marks):
        self.marks = marks

    def run(self):
        self.send_output("Setting up macro cavebot.")
        cavebot_service = CavebotService()
        self.send_output("Initializing cavebot.")
        while True:
            for mark in self.marks:
                self.wait_if_paused()
                self.send_output(f"Doing mark {mark.name}.")
                cavebot_service.do_mark(mark)
