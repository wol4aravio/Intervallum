import pytest
from numpy.testing import assert_almost_equal

from intervallum.interval import Interval


@pytest.fixture(scope="session")
def i1() -> Interval:
    return Interval(0.0, 1.0)


@pytest.fixture(scope="session")
def i2() -> Interval:
    return Interval(-1.0, 2.0)


@pytest.fixture(scope="session")
def i3() -> Interval:
    return Interval(-3.0, -1.0)


def test_interval_creation(i1: Interval):
    assert_almost_equal(i1.lb, 0.0)
    assert_almost_equal(i1.ub, 1.0)

    i2 = Interval(-1e-8, 1e-8)
    assert_almost_equal(i2.lb, 0.0)
    assert_almost_equal(i2.ub, 0.0)


def test_addition(i1: Interval, i2: Interval, i3: Interval):
    i12 = i1 + i2
    assert_almost_equal(i12.lb, -1)
    assert_almost_equal(i12.ub, 3.0)

    i13 = i1 + i3
    assert_almost_equal(i13.lb, -3)
    assert_almost_equal(i13.ub, 0.0)
