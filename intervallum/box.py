from copy import copy

import numpy as np
from typing import Union, List, Callable, Tuple, NamedTuple
import functools

from intervallum.interval import Interval, IntervalNumber


BoxVector = Union["Box", np.ndarray]


def reduce_result(f: Callable[..., "Box"]) -> Callable[..., BoxVector]:
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        b = f(*args, **kwargs)
        return b._try_to_reduce()
    return wrapper


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

    def __len__(self) -> int:
        return len(self.__components)

    @property
    def middle(self) -> np.ndarray:
        return np.array([i.middle if isinstance(i, Interval) else i for i in self.__components])

    @property
    def width(self) -> Tuple[List[int], float]:
        widths = [i.width if isinstance(i, Interval) else 0 for i in self.__components]
        max_width = max(widths)
        return [i for i, w in enumerate(widths) if w == max_width], max_width

    def _try_to_reduce(self) -> BoxVector:
        if self.width[1] == 0.0:
            return self.middle
        else:
            return copy(self)

    @reduce_result
    def __mul__(self, other: float) -> "Box":
        return Box(*[v * other for v in self.__components])

    @reduce_result
    def __rmul__(self, other: float) -> "Box":
        return self * other

    @reduce_result
    def __truediv__(self, other: float) -> "Box":
        return self * (1.0 / other)

    @reduce_result
    def __neg__(self):
        return self * (-1.0)

    # @reduce_result
    # def __add__(self, other: BoxVector) -> "Box":
    #     dim = len(self)
    #     if dim != len(other):
    #         raise BoxExceptions.DifferentDimensionality(len(self), len(other))
    #     return Box(*[self[i] + other[i] for i in range(dim)])
    #
    # @reduce_result
    # def __radd__(self, other: BoxVector) -> "Box":
    #     return self + other


class BoxExceptions:
    class DifferentDimensionality(Exception):
        def __init__(self, dim_1: int, dim_2: int):
            super().__init__(f"Input vectors have different dims: {dim_1} and {dim_2}")
