from random import randint
from math import floor
import time

from otsourcing.data_model.map_mark import Mark
from otsourcing.gui.window_utils import locateCenterOnScreen, click
from otsourcing.settings import map_region, resources_folder, map_center


def click_on_mark(mark: Mark):
    print(f"entering click_on_mark {mark=}")
    mark_image = f"{resources_folder}/map_marks/mark_{mark.i_id}_{mark.j_id}.png"
    pos = locateCenterOnScreen(mark_image, region=map_region, minSearchTime=0)
    if not pos:
        mark.on_img_not_found(mark)
    else:
        x_var = randint(-mark.max_x_var, mark.max_x_var)
        y_var = randint(-mark.max_y_var, mark.max_y_var)
        print(f"{pos=} {x_var=} {y_var=}")
        click(pos.x + x_var, pos.y + y_var)
        print("clicked")
        print("exiting click_on_mark")


def is_close(mark_pos, threshold):
    delta_x = abs(mark_pos.x - map_center[0])
    delta_y = abs(mark_pos.y - map_center[1])
    return delta_x < threshold and delta_y < threshold


def click_mark_with_retry(mark: Mark):
    print(f"entering click_mark_with_retry {mark=}")
    mark_image = f"{resources_folder}/map_marks/mark_{mark.i_id}_{mark.j_id}.png"
    pos = locateCenterOnScreen(mark_image, region=map_region, minSearchTime=0)
    if not pos:
        mark.on_img_not_found(mark)
        return
    div_factor = 1
    while not is_close(pos, 5):
        yield None
        x_var = floor(randint(-mark.max_x_var, mark.max_x_var) / div_factor)
        y_var = floor(randint(-mark.max_y_var, mark.max_y_var) / div_factor)
        click(pos.x + x_var, pos.y + y_var)
        print("clicked")
        time.sleep(3)
        pos = locateCenterOnScreen(mark_image, region=map_region, minSearchTime=0)
        div_factor = div_factor * 2
    print("exiting click_mark_with_retry")
