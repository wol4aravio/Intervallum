from typing import List

from intervallum.interval import IntervalNumber


class Box:

    __slots__ = ["__components"]

    def __init__(self, *args: IntervalNumber):
        self.__components = args

    def __getitem__(self, item: int) -> IntervalNumber:
        return self.__components[item]
