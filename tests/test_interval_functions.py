import numpy as np

from intervallum.interval import Interval
from intervallum.box import Box
from intervallum.interval_functions import hausdorff_distance
from intervallum.inclusion_functions import RS_subinclusion_function


def test_base():
    def f(x: np.ndarray):
        return x[0] ** 2 - x[0] ** 2 + x[1] ** 2
    rs_f_10 = RS_subinclusion_function(f, number_of_samples=10)
    rs_f_100 = RS_subinclusion_function(f, number_of_samples=100)
    rs_f_10000 = RS_subinclusion_function(f, number_of_samples=10000)

    b = Box(Interval(1, 2), Interval(-1.0, 1.0))
    target_interval = Interval(0.0, 1.0)

    test_interval_10 = rs_f_10(b)
    test_interval_100 = rs_f_100(b)
    test_interval_10000 = rs_f_10000(b)

    h_10 = hausdorff_distance(target_interval, test_interval_10)
    h_100 = hausdorff_distance(target_interval, test_interval_100)
    h_10000 = hausdorff_distance(target_interval, test_interval_10000)

    assert h_10 > h_100
    assert h_100 > h_10000
    assert h_10000 < 1e-3
