from typing import Union


IntervalNumber = Union["Interval", float]

class Interval:

    _reduction_width: float = 1e-5
    _admissible_error: float = 1e-7

    __slots__ = ["__lb", "__ub"]

    def __init__(self, lower_bound: float, upper_bound: float, point_value: float = None, reduce: bool = True):
        if point_value:
            self.__lb = point_value
            self.__ub = point_value
        else:
            if lower_bound > upper_bound:
                raise IntervalExceptions.WrongBoundsException(lower_bound, upper_bound)
            self.__lb = lower_bound
            self.__ub = upper_bound
            if reduce and (upper_bound - lower_bound) < Interval._reduction_width:
                self._reduce()

    def _try_to_reduce(self, reduction_width: float = _reduction_width) -> None:
        if reduce and (upper_bound - lower_bound) < Interval._reduction_width:
            middle = 0.5 * (self.__lb + self.__ub)
            self.__lb = middle
            self.__ub = middle

    @property
    def lb(self):
        return self.__lb

    @lb.setter
    def lb(self, lower_bound: float):
        if lower_bound > self.__ub:
            raise IntervalExceptions.WrongBoundsException(lower_bound, self.__ub)
        else:
            self.__lb = lower_bound

    @property
    def ub(self):
        return self.__ub

    @ub.setter
    def ub(self, upper_bound: float):
        if upper_bound < self.__lb:
            raise IntervalExceptions.WrongBoundsException(self.__lb, upper_bound)
        else:
            self.__ub = upper_bound

    def __str__(self) -> str:
        return f"[{self._lb}; {self._ub}]"

    def __repr__(self) -> str:
        return self.__str__()


class IntervalExceptions:
    class WrongBoundsException(Exception):
        def __init__(self, received_lb: float, received_ub: float):
            super().__init__(f"Improper interval [{received_lb}; {received_ub}]")
