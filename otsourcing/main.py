from typing import Set
from multiprocessing import Process

from otsourcing.gui.gui import start_gui
from otsourcing.app import OtSorcing

process_pool: Set[Process] = set()


def start_app():
    start_gui(process_pool=process_pool, ot_sorcing=OtSorcing())
