from copy import copy
import math

import pytest
from numpy.testing import assert_almost_equal

from intervallum.interval import Interval, IntervalExceptions
from intervallum.interval_functions import *


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

    i.lb = 1.5
    assert_almost_equal(i.lb, 1.5)
    with pytest.raises(IntervalExceptions.WrongBoundsException):
        i.lb = 3

    i.ub = 1.9
    assert_almost_equal(i.ub, 1.9)
    with pytest.raises(IntervalExceptions.WrongBoundsException):
        i.ub = 0


def test_string_representation(i1: Interval, i4: Interval, i6: Interval):
    assert str(i1) == "[-1.0; 2.0]"
    assert str(i4) == "[5.0; 5.1]"
    assert i6.__repr__() == "[-2.0; 0.0]"


def test_equality(i1: Interval, i2: Interval):
    assert i1 == copy(i1)
    assert i1 != i2
    with pytest.raises(NotImplementedError):
        _ = i1 == "Interval"


def test_middle(i2: Interval, i3: Interval):
    assert_almost_equal(i2.middle, -0.5)
    assert_almost_equal(i3.middle, 1.5)


def test_width(i7: Interval, i4: Interval):
    assert_almost_equal(i7.width, 3)
    assert_almost_equal(i4.width, 0.1)


def test_reduction(i4: Interval):
    assert i4 == i4._try_to_reduce()
    i = Interval(1.0, 1.0 + 1e-7)
    assert i._try_to_reduce() == Interval.from_point(i.middle)


def test_addition(i1: Interval, i2: Interval, i3: Interval, i4: Interval, i5: Interval):
    assert (i1 + 2.0) == Interval(1.0, 4.0)
    assert (2.0 + i1) == Interval(1.0, 4.0)
    assert (i1 + i2) == Interval(-5.0, 5.0)
    assert (i2 + i3) == Interval(-3.0, 5.0)
    assert (i5 + i4) == Interval(-1.0, 0.1)


def test_subtraction(i1: Interval, i2: Interval, i3: Interval, i4: Interval, i5: Interval):
    assert (i1 - 1.0) == Interval(-2.0, 1.0)
    assert (1.0 - i1) == Interval(-1.0, 2.0)
    assert (i1 - i2) == Interval(-4.0, 6.0)
    assert (i2 - i3) == Interval(-6.0, 2.0)
    assert (i5 - i4) == Interval(-11.1, -10.0)


def test_multiplication(i1: Interval, i2: Interval, i3: Interval, i4: Interval, i5: Interval):
    assert (i1 * (-1)) == Interval(-2.0, 1.0)
    assert ((-1.0) * i1) == Interval(-2.0, 1.0)
    assert (i1 * i2) == Interval(-8.0, 6.0)
    assert (i2 * i3) == Interval(-8.0, 6.0)
    assert (i5 * i4) == Interval(-30.6, -25.0)


def test_division(i1: Interval, i2: Interval, i3: Interval, i4: Interval, i5: Interval, i6: Interval, i7: Interval):
    assert (i1 / 2.0) == Interval(-0.5, 1.0)
    assert (2.0 / i1) == Interval(-math.inf, math.inf)
    assert (i1 / i2) == Interval(-math.inf, math.inf)
    assert (i2 / i3) == Interval(-4.0, 3.0)
    assert (i1 / i5) == Interval(-0.4, 0.2)
    assert (i3 / i6) == Interval(-math.inf, -0.5)
    assert (i5 / i7) == Interval(-math.inf, -5.0 / 3.0)


def test_power(i1: Interval, i2: Interval, i5: Interval):
    assert (i1 ** 2) == Interval(0.0, 4.0)
    assert (i2 ** 3) == Interval(-64.0, 27.0)
    assert (i5 ** 0) == Interval(1.0, 1.0)


def test_sin(i1: Interval, i2: Interval, i3: Interval, i6: Interval):
    assert sin(i1) == Interval(math.sin(-1.0), 1.0)
    assert sin(i2) == Interval(-1.0, 1.0)
    assert sin(i3) == Interval(math.sin(1.0), 1.0)
    assert sin(i6) == Interval(-1.0, 0.0)


def test_cos(i1: Interval, i2: Interval, i3: Interval, i6: Interval):
    assert cos(i1) == Interval(math.cos(2.0), 1.0)
    assert cos(i2) == Interval(-1.0, 1.0)
    assert cos(i3) == Interval(math.cos(2.0), math.cos(1.0))
    assert cos(i6) == Interval(math.cos(-2.0), 1.0)
