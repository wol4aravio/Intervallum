from typing import Union


_IntervalNumber = Union["Interval", float]


class Interval:

    _reduce_intervals_to_numbers: bool = True
    _reduction_width: float = 1e-5
    _admissible_error: float = 1e-7

    __slots__ = ["__lb", "__ub"]

    def __init__(self, lower_bound: float, upper_bound: float, point_value: float = None):
        if point_value:
            self.__lb = point_value
            self.__ub = point_value
        else:
            if lower_bound > upper_bound:
                raise IntervalExceptions.WrongBoundsException(lower_bound, upper_bound)
            self.__lb = lower_bound
            self.__ub = upper_bound

    def __str__(self) -> str:
        return f"[{self.__lb}; {self.__ub}]"

    def __repr__(self) -> str:
        return self.__str__()

    def copy(self) -> "Interval":
        return Interval(self.__lb, self.__ub)

    def _try_to_reduce(self) -> _IntervalNumber:
        if (self.__ub - self.__lb) < Interval._reduction_width:
            return 0.5 * (self.__lb + self.__ub)
        else:
            return self.copy()

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


class IntervalExceptions:
    class WrongBoundsException(Exception):
        def __init__(self, received_lb: float, received_ub: float):
            super().__init__(f"Improper interval [{received_lb}; {received_ub}]")
