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

    def __getitem__(self, item: int) -> IntervalNumber:
        return self.__components[item]

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
    #     if (self.__ub - self.__lb) < IntervalConstants._reduction_width:
    #         return 0.5 * (self.__lb + self.__ub)
    #     else:
    #         return copy(self)
