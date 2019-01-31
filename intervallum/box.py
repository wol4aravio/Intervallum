from typing import List

from intervallum.interval import IntervalNumber


class Box:

    __slots__ = ["__components"]

    def __init__(self, components: List[IntervalNumber]):
        self.__components = components

    def __getitem__(self, item: int) -> IntervalNumber:
        return self.__components[item]

    def __setitem__(self, key, value):
        raise NotImplementedError
