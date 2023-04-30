import time
import pyautogui
import pyscreeze
from pyscreeze import RGB
from otsourcing.data_model.amulet import Amulet
from otsourcing.gui.window_utils import only_if_window_focused, is_gray


class SsaService:
    def __init__(
        self,
        ssa_key,
        default_amulet_key,
        is_full_ssa,
        ssa_cd,
        amulet: Amulet,
    ):
        self.ssa_key = ssa_key
        self.default_amulet_key = default_amulet_key
        self.is_full_ssa = is_full_ssa
        self.ssa_cd = ssa_cd
        self.amulet = amulet

        self.ssa_enable = False
        self.ssa_equiped = False
        self.ssa_timer = time.perf_counter()

    @only_if_window_focused
    def handle_ssa(self):
        health_bar_ssa_color = RGB(*pyscreeze.pixel(*self.amulet.ssa_pixel_health_pos))
        if self.is_full_ssa:
            self.equip_ssa()
        elif is_gray(health_bar_ssa_color) and self.ssa_enable:
            self.equip_ssa()
        else:
            self.equip_default_amulet()

    def equip_ssa(self):
        current_timer = time.perf_counter()
        diff = current_timer - self.ssa_timer
        if not self.ssa_enable:
            return
        if diff < self.ssa_cd:
            return
        amulet_slot_color = RGB(*pyscreeze.pixel(*self.amulet.ssa_pixel_pos))
        if amulet_slot_color != self.amulet.ssa_pixel_color:
            pyautogui.press(self.ssa_key)
            self.ssa_timer = time.perf_counter()
            self.ssa_equiped = True

    def equip_default_amulet(self):
        amulet_slot_color = RGB(*pyscreeze.pixel(*self.amulet.ssa_pixel_pos))
        if self.ssa_equiped and amulet_slot_color != self.amulet.ssa_pixel_color:
            pyautogui.press(self.default_amulet_key)
            self.ssa_equiped = False
