import pytest
from numpy.testing import assert_almost_equal

from intervallum.interval import Interval
from intervallum.interval import IntervalExceptions


@pytest.fixture(scope="session")
def i1() -> Interval:
    return Interval(-1.0, 2.0)


@pytest.fixture(scope="session")
def i2() -> Interval:
    return Interval(-4.0, 3.0)


@pytest.fixture(scope="session")
def i3() -> Interval:
    return Interval(1.0, 2.0)


@pytest.fixture(scope="session")
def i4() -> Interval:
    return Interval(5.0, 5.1)


@pytest.fixture(scope="session")
def i5() -> Interval:
    return Interval(-6.0, -5.0)


@pytest.fixture(scope="session")
def i6() -> Interval:
    return Interval(-2.0, 0.0)


@pytest.fixture(scope="session")
def i7() -> Interval:
    return Interval(0.0, 3.0)


def test_interval_exceptions():
    with pytest.raises(IntervalExceptions.WrongBoundsException):
        _ = Interval(1, -1)


def test_string_representation(i1: Interval, i4: Interval, i6: Interval):
    assert str(i1) == '[-1.0; 2.0]'
    assert str(i4) == '[5.0; 5.1]'
    assert str(i6) == '[-2.0; 0.0]'


def test_interval_creation(i1: Interval):
    assert_almost_equal(i1.__lb, -1.0)
    assert_almost_equal(i1.__ub, 2.0)

    i2 = Interval(-1e-8, 1e-8)
    assert_almost_equal(i2.__lb, 0.0)
    assert_almost_equal(i2.__ub, 0.0)


