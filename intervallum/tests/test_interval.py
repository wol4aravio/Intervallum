from copy import copy

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
    i = Interval(1, 2)
    with pytest.raises(IntervalExceptions.WrongBoundsException):
        i.lb = 3
    with pytest.raises(IntervalExceptions.WrongBoundsException):
        i.ub = 0


def test_string_representation(i1: Interval, i4: Interval, i6: Interval):
    assert str(i1) == '[-1.0; 2.0]'
    assert str(i4) == '[5.0; 5.1]'
    assert str(i6) == '[-2.0; 0.0]'


def test_middle(i2: Interval, i3: Interval):
    assert_almost_equal(i2.middle, -0.5)
    assert_almost_equal(i3.middle, 1.5)


def test_width(i7: Interval, i4: Interval):
    assert_almost_equal(i7.width, 3)
    assert_almost_equal(i4.width, 0.1)


def test_reduction(i7: Interval):
    i = copy(i7)
    assert i == i._try_to_reduce()

