import pytest
from numpy.testing import assert_almost_equal

from intervallum.interval import Interval


@pytest.fixture(scope="session")
def i1() -> Interval:
    return Interval(0.0, 1.0)


def test_interval_creation(i1: Interval):
    assert_almost_equal(i1.lb, 0.0)
    assert_almost_equal(i1.ub, 1.0)

    i2 = Interval(-1e-8, 1e-8)
    assert_almost_equal(i2.lb, 0.0)
    assert_almost_equal(i2.ub, 0.0)
