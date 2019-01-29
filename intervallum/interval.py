from copy import copy
from typing import Any, Union, Callable
import functools


IntervalNumber = Union["Interval", float]


def reduce_result(f: Callable[..., "Interval"]) -> Callable[..., "Interval"]:
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        i: Interval = f(*args, **kwargs)
        return i._try_to_reduce() if Interval._reduce_intervals_to_numbers else i

    return wrapper


class Interval:

    _reduce_intervals_to_numbers: bool = True
    _reduction_width: float = 1e-5
    _admissible_error: float = 1e-7

    __slots__ = ["__lb", "__ub"]

    def __init__(self, lower_bound: float, upper_bound: float):
        if lower_bound > upper_bound:
            raise IntervalExceptions.WrongBoundsException(lower_bound, upper_bound)
        self.__lb = lower_bound
        self.__ub = upper_bound

    @classmethod
    def from_point(cls, point_value: float):
        return cls(lower_bound=point_value, upper_bound=point_value)

    def __str__(self) -> str:
        return f"[{self.__lb}; {self.__ub}]"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def lb(self) -> float:
        return self.__lb

    @lb.setter
    def lb(self, lower_bound: float):
        if lower_bound > self.__ub:
            raise IntervalExceptions.WrongBoundsException(lower_bound, self.__ub)
        else:
            self.__lb = lower_bound

    @property
    def ub(self) -> float:
        return self.__ub

    @ub.setter
    def ub(self, upper_bound: float):
        if upper_bound < self.__lb:
            raise IntervalExceptions.WrongBoundsException(self.__lb, upper_bound)
        else:
            self.__ub = upper_bound

    @property
    def middle(self) -> float:
        return 0.5 * (self.__lb + self.__ub)

    @property
    def width(self) -> float:
        return self.__ub - self.__lb

    def __copy__(self):
        return Interval(self.__lb, self.__ub)

    def _try_to_reduce(self) -> IntervalNumber:
        if (self.__ub - self.__lb) < Interval._reduction_width:
            return 0.5 * (self.__lb + self.__ub)
        else:
            return copy(self)

    @staticmethod
    @reduce_result
    def inner_subtraction(i1: IntervalNumber, i2: IntervalNumber) -> IntervalNumber:
        _i1: Interval = i1 if isinstance(i1, Interval) else Interval.from_point(i1)
        _i2: Interval = i2 if isinstance(i2, Interval) else Interval.from_point(i2)
        return Interval(_i1.__lb - _i2.__lb, _i1.__ub - _i2.__ub)

    def __lshift__(self, other: IntervalNumber) -> IntervalNumber:
        return Interval.inner_subtraction(self, other)

    def __eq__(self, other: object) -> bool:
        if not (isinstance(other, float) or isinstance(other, Interval)):
            raise NotImplemented()
        else:
            distance: IntervalNumber = self << other
            if isinstance(distance, Interval):
                distance = distance.width
            else:
                distance = abs(distance)
            return distance <= Interval._admissible_error


class IntervalExceptions:
    class WrongBoundsException(Exception):
        def __init__(self, received_lb: float, received_ub: float):
            super().__init__(f"Improper interval [{received_lb}; {received_ub}]")
