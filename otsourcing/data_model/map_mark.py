from dataclasses import dataclass

from typing import Callable


def fail(mark):
    raise RuntimeError(f'img not found {mark=}')


def skip(mark):  # no qa
    ...


@dataclass
class Mark:
    i_id: int
    j_id: int
    name: str = None
    max_x_var: int = 5
    max_y_var: int = 5
    special_action: Callable = None
    delay: int = 2
    check_battle: bool = True
    on_img_not_found: Callable = fail
