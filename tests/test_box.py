from copy import copy

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from intervallum.interval import Interval
from intervallum.box import Box
from intervallum.box_functions import bisect, shrink, constrain


@pytest.fixture(scope="session")
def b1() -> Box:
    return Box(1.0, Interval(2.0, 3.0), Interval(4.0, 7.0), 9)


@pytest.fixture(scope="session")
def b2() -> Box:
    return Box(Interval(1.0, 2.0), Interval(2.0, 4.0), Interval(5.0, 8.0))


@pytest.fixture(scope="session")
def b3() -> Box:
    return Box(Interval(1.0, 2.0), Interval(2.0, 3.0), Interval(3.0, 3.5))


@pytest.fixture(scope="session")
def b4() -> Box:
    return Box(Interval(1.0, 1.0), Interval(2.0, 2.0), Interval(3.0, 3.0))


def test_base(b1: Box):
    assert_almost_equal(b1[0], 1.0)
    assert b1[1] == Interval(2.0, 3.0)


def test_str_repr(b1: Box):
    assert str(b1) == "1.0 x [2.0; 3.0] x [4.0; 7.0] x 9"
    assert b1.__repr__() == "1.0 x [2.0; 3.0] x [4.0; 7.0] x 9"


def test_dim(b1: Box, b2: Box):
    assert len(b1) == 4
    assert len(b2) == 3


def test_lb_ub(b1: Box):
    assert_almost_equal(b1.lb, np.array([1, 2, 4, 9]))
    assert_almost_equal(b1.ub, np.array([1, 3, 7, 9]))


def test_middle(b1: Box, b2: Box):
    assert_almost_equal(b1.middle, np.array([1, 2.5, 5.5, 9]))
    assert_almost_equal(b2.middle, np.array([1.5, 3.0, 6.5]))


def test_width(b1: Box, b2: Box, b3: Box):
    i1, w1 = b1.width
    assert i1 == [2]
    assert_almost_equal(w1, 3.0)

    i2, w2 = b2.width
    assert i2 == [2]
    assert_almost_equal(w2, 3.0)

    i3, w3 = b3.width
    assert i3 == [0, 1]
    assert_almost_equal(w3, 1.0)


def test_eq(b1: Box, b2: Box):
    assert b1 == copy(b1)
    assert b1 != b2
    with pytest.raises(NotImplementedError):
        _ = b1 == "Box"


def test_try_to_reduce(b1: Box, b4: Box):
    assert b1._try_to_reduce() == b1
    assert b1._try_to_reduce().dtype != float
    assert b4._try_to_reduce().dtype == float


def test_multiply_by_scalar(b1: Box):
    assert b1 * 2.0 == 2.0 * b1
    assert b1 * 2.0 == b1 / 0.5
    assert b1 * 2.0 == Box(2.0, Interval(4.0, 6.0), Interval(8.0, 14.0), 18)
    assert -b1 == Box(-1.0, Interval(-3.0, -2.0), Interval(-7.0, -4.0), -9)
    assert isinstance(b1 * 1e-9, np.ndarray)


def test_addition(b1: Box, b2: Box, b3: Box):
    with pytest.raises(ValueError):
        _ = b1 + b2
    assert b3 + np.array([1, 1, 1]) == Box(Interval(2.0, 3.0), Interval(3.0, 4.0), Interval(4.0, 4.5))
    assert np.array([1, 1, 1]) + b3 == b3 + np.array([1, 1, 1])
    assert b3 - np.array([1, 1, 1]) == Box(Interval(0.0, 1.0), Interval(1.0, 2.0), Interval(2.0, 2.5))
    assert np.array([1, 1, 1]) - b3 == Box(Interval(-1.0, 0.0), Interval(-2.0, -1.0), Interval(-2.5, -2.0))
    assert b2 - b2 != Box(0.0, 0.0, 0.0)
    assert b2 * 2.0 == b2 + b2


def test_split(b1: Box):
    assert_almost_equal(bisect(np.array([1, 2, 3]))[1][0], np.array([1, 2, 3]))
    assert_almost_equal(bisect(np.array([1, 2, 3]))[1][1], np.array([1, 2, 3]))
    assert bisect(b1, 0)[0] == 0
    assert bisect(b1)[0] == 2
    assert bisect(b1, 0)[1][0] == b1
    assert bisect(b1, 0)[1][1] == b1
    assert bisect(b1)[1][0] == Box(1.0, Interval(2.0, 3.0), Interval(4.0, 5.5), 9)
    assert bisect(b1)[1][1] == Box(1.0, Interval(2.0, 3.0), Interval(5.5, 7.0), 9)


def test_constrain(b3: Box):
    assert constrain(b3, area=[(3.0, 4.0), (2.1, 2.9), (0.0, 1.0)]) == Box(3.0, Interval(2.1, 2.9), 1.0)


def test_shrink(b1: Box):
    assert shrink(b1, alpha=0.5) == Box(1.0, Interval(2.25, 2.75), Interval(4.75, 6.25), 9.0)
    assert np.all(shrink(b1.middle, alpha=0.0) == b1.middle)
    assert np.all(shrink(b1, alpha=0.0) == b1.middle)
    assert shrink(b1, alpha=0.5, shrink_components=[0, 3]) == b1
