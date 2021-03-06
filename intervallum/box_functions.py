from copy import copy

from typing import List, Tuple
import random

from intervallum.box import Box, BoxVector
from intervallum.interval_functions import split as i_split
from intervallum.interval_functions import shrink as i_shrink
from intervallum.interval_functions import constrain as i_constrain


def split(b: BoxVector, ratios: List[float], split_id: int = None) -> Tuple[int, List[BoxVector]]:
    if not isinstance(b, Box):
        copies = []
        for _ in range(len(ratios)):
            copies.append(b.copy())
        return random.choice(range(len(b))), copies
    if split_id is None:
        ids, w = b.width
        id_ = random.choice(ids)
    else:
        id_ = split_id

    part_1 = [copy(i) for i in b[:id_]]
    part_2 = [copy(i) for i in b[(id_ + 1):]]

    boxes = [Box(*(part_1 + [i] + part_2)) for i in i_split(b[id_], ratios)]
    boxes = [b._try_to_reduce() for b in boxes]
    return id_, boxes


def bisect(b: BoxVector, split_id: int = None) -> Tuple[int, List[BoxVector]]:
    return split(b, [1.0, 1.0], split_id)


def constrain(b: BoxVector, area: List[Tuple[float, float]]) -> BoxVector:
    new_components = list()
    for id_, (min_, max_) in enumerate(area):
        new_components.append(i_constrain(b[id_], min_, max_))
    return Box(*new_components)._try_to_reduce()


def shrink(b: BoxVector, alpha: float, shrink_components: List[int] = None) -> BoxVector:
    new_components = list()
    for id_, c in enumerate(b):
        if (shrink_components is None) or (id_ in shrink_components):
            new_components.append(i_shrink(c, alpha))
        else:
            new_components.append(copy(c))
    return Box(*new_components)._try_to_reduce()
