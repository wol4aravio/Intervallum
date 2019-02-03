from copy import copy

import pytest
from numpy.testing import assert_almost_equal

from intervallum.interval import _try_to_reduce
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


def test_lt(i1: Interval, i2: Interval, i6: Interval, i7: Interval):
    assert i2 < i1
    assert i2 < -1
    assert i6 < i7


def test_le(i1: Interval, i2: Interval):
    assert i2 <= i1
    assert i2 <= -1
    assert i2 <= Interval(-4.0, 2.0)


def test_gt(i1: Interval, i2: Interval, i6: Interval, i7: Interval):
    assert i1 > i2
    assert i1 > -4
    assert i7 > i6


def test_ge(i1: Interval, i2: Interval):
    assert i1 >= i2
    assert i1 >= -4
    assert Interval(-4.0, 2.0) >= i2


def test_middle(i2: Interval, i3: Interval):
    assert_almost_equal(i2.middle, -0.5)
    assert_almost_equal(i3.middle, 1.5)


def test_width(i7: Interval, i4: Interval):
    assert_almost_equal(i7.width, 3)
    assert_almost_equal(i4.width, 0.1)


def test_reduction(i4: Interval):
    assert i4 == _try_to_reduce(i4)
    i = Interval(1.0, 1.0 + 1e-7)
    assert _try_to_reduce(i) == Interval.from_point(i.middle)


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
    for i in [i1, i2, i3, i6]:
        assert_almost_equal(math.sin(i.lb), sin(i.lb))
    assert sin(i1) == Interval(math.sin(-1.0), 1.0)
    assert sin(i2) == Interval(-1.0, 1.0)
    assert sin(i3) == Interval(math.sin(1.0), 1.0)
    assert sin(i6) == Interval(-1.0, 0.0)


def test_cos(i1: Interval, i2: Interval, i3: Interval, i6: Interval):
    for i in [i1, i2, i3, i6]:
        assert_almost_equal(math.cos(i.lb), cos(i.lb))
    assert cos(i1) == Interval(math.cos(2.0), 1.0)
    assert cos(i2) == Interval(-1.0, 1.0)
    assert cos(i3) == Interval(math.cos(2.0), math.cos(1.0))
    assert cos(i6) == Interval(math.cos(-2.0), 1.0)


def test_abs(i1: Interval, i2: Interval, i3: Interval, i4: Interval, i5: Interval, i6: Interval, i7: Interval):
    for i in [i1, i2, i3, i4, i5, i6, i7]:
        assert_almost_equal(math.fabs(i.lb), abs(i.lb))
    assert abs(i1) == Interval(0.0, 2.0)
    assert abs(i2) == Interval(0.0, 4.0)
    assert abs(i3) == Interval(1.0, 2.0)
    assert abs(i4) == Interval(5.0, 5.1)
    assert abs(i5) == Interval(5.0, 6.0)
    assert abs(i6) == Interval(0.0, 2.0)
    assert abs(i7) == Interval(0.0, 3.0)


def test_exp(i1: Interval, i2: Interval, i3: Interval):
    for i in [i1, i2, i3]:
        assert_almost_equal(math.exp(i.lb), exp(i.lb))
    assert exp(i1) == Interval(math.exp(-1.0), math.exp(2.0))
    assert exp(i2) == Interval(math.exp(-4.0), math.exp(3.0))
    assert exp(i3) == Interval(math.exp(1.0), math.exp(2.0))


def test_sqrt(i1: Interval, i3: Interval, i5: Interval):
    assert_almost_equal(math.sqrt(i3.lb), sqrt(i3.lb))
    assert sqrt(i1) == Interval(0.0, math.sqrt(2.0))
    assert sqrt(i3) == Interval(math.sqrt(1.0), math.sqrt(2.0))
    with pytest.raises(IntervalExceptions.OperationIsNotDefined):
        _ = sqrt(i5)


def test_log(i1: Interval, i2: Interval, i3: Interval, i4: Interval, i5: Interval, i6: Interval, i7: Interval):
    for i in [i3, i4]:
        assert_almost_equal(math.log(i.lb), log(i.lb))
    assert log(i1) == Interval(-math.inf, math.log(2.0))
    assert log(i2) == Interval(-math.inf, math.log(3.0))
    assert log(i3) == Interval(math.log(1.0), math.log(2.0))
    assert log(i4) == Interval(math.log(5.0), math.log(5.1))
    with pytest.raises(IntervalExceptions.OperationIsNotDefined):
        _ = log(i5)
    with pytest.raises(IntervalExceptions.OperationIsNotDefined):
        _ = log(i6)
    assert log(i7) == Interval(-math.inf, math.log(3.0))


def test_constrain(i1: Interval, i4: Interval, i7: Interval):
    assert i1.constrain(1.5, 3.0) == Interval(1.5, 2.0)
    assert i4.constrain(1.5, 3.0) == Interval(3.0, 3.0)
    assert i7.constrain(-10, 3.0) == i7


def test_splitting(i1: Interval):
    assert i1.bisect()[0] == Interval(-1.0, 0.5)
    assert i1.bisect()[1] == Interval(0.5, 2.0)
    assert i1.split([1.0, 2.0])[0] == Interval(-1.0, 0.0)
    assert i1.split([1.0, 2.0])[1] == Interval(0.0, 2.0)
