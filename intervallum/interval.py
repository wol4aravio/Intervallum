from typing import Union


class Interval:

    _reduction_width: float = 1e-5

    __slots__ = ["lb", "ub"]

    def __init__(self, lower_bound: float, upper_bound: float, reduce: bool = True):
        if reduce and (upper_bound - lower_bound) < Interval._reduction_width:
            middle = 0.5 * (lower_bound + upper_bound)
            self.lb = middle
            self.ub = middle
        else:
            self.lb = lower_bound
            self.ub = upper_bound

    def __add__(self, other: Union["Interval", float]) -> "Interval":
        if isinstance(other, Interval):
            return Interval(self.lb + other.lb, self.ub + other.ub)
        else:
            return Interval(self.lb + other, self.ub + other)

    def __radd__(self, other: Union["Interval", float]) -> "Interval":
        return self + other
