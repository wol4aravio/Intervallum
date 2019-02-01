from copy import copy

import numpy as np
from typing import Union, List, Callable, Tuple
import functools

from intervallum.interval import Interval, IntervalNumber


BoxVector = Union["Box", np.ndarray]


# def reduce_result(f: Callable[..., "Interval"]) -> Callable[..., IntervalNumber]:
#     @functools.wraps(f)
#     def wrapper(*args, **kwargs):
#         i = f(*args, **kwargs)
#         return i._try_to_reduce() if IntervalConstants._reduce_intervals_to_numbers else i
#     return wrapper


class Box:

    __slots__ = ["__components"]

    def __init__(self, *args: IntervalNumber):
        self.__components = args

    def __str__(self) -> str:
        return " x ".join(v.__str__() for v in self.__components)

    def __repr__(self) -> str:
        return " x ".join(v.__repr__() for v in self.__components)

    def __getitem__(self, item: int) -> IntervalNumber:
        return self.__components[item]

    def __copy__(self) -> "Box":
        return Box(*[copy(v) for v in self.__components])

    def __eq__(self, other: object) -> bool:
        if not (isinstance(other, np.ndarray) or isinstance(other, Box)):
            raise NotImplementedError()
        for v1, v2 in zip(self.__components, other.__components if isinstance(other, Box) else other):
            if v1 != v2:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def dim(self) -> int:
        return len(self.__components)

    @property
    def middle(self) -> np.ndarray:
        return np.array([i.middle if isinstance(i, Interval) else i for i in self.__components])

    @property
    def width(self) -> Tuple[List[int], float]:
        widths = [i.width if isinstance(i, Interval) else 0 for i in self.__components]
        max_width = max(widths)
        return [i for i, w in enumerate(widths) if w == max_width], max_width

    # def _try_to_reduce(self) -> BoxVector:
    #     if self.width == 0.0:
    #         return self.middle
    #     else:
    #         return copy(self)
