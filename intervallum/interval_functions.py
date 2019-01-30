from typing import Callable, List, Tuple
import math

from intervallum.interval import Interval
from intervallum.interval import reduce_result, monotonic


def _get_points_for_trig(left: float, right: float) -> List[float]:
    c = 0.5 * math.pi
    left_bound = int(math.ceil(left / c))
    right_bound = int(math.floor(right / c))
    return [left, right] + list(map(lambda v: c * v, range(left_bound, right_bound + 1)))


@reduce_result
@monotonic
def sin(i: "Interval") -> Tuple[Callable[[float], float], List[float]]:
    if i.width >= 2 * math.pi:
        return lambda x: x, [-1.0, 1.0]
    else:
        return lambda x: math.sin(x), _get_points_for_trig(i.lb, i.ub)
