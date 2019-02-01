from copy import copy

import pytest
import numpy as np
from numpy.testing import assert_almost_equal

from intervallum.interval import Interval
from intervallum.box import Box


@pytest.fixture(scope="session")
def b1() -> Box:
    return Box(1.0, Interval(2.0, 3.0), Interval(4.0, 7.0), 9)


@pytest.fixture(scope="session")
def b2() -> Box:
    return Box(Interval(1.0, 2.0), Interval(2.0, 4.0), Interval(5.0, 8.0))


@pytest.fixture(scope="session")
def b3() -> Box:
    return Box(Interval(1.0, 2.0), Interval(2.0, 3.0), Interval(3.0, 3.5))


def test_base(b1: Box):
    assert_almost_equal(b1[0], 1.0)
    assert b1[1] == Interval(2.0, 3.0)


def test_str_repr(b1: Box):
    assert str(b1) == "1.0 x [2.0; 3.0] x [4.0; 7.0] x 9"
    assert b1.__repr__() == "1.0 x [2.0; 3.0] x [4.0; 7.0] x 9"


def test_dim(b1: Box, b2: Box):
    assert b1.dim == 4
    assert b2.dim == 3


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

# def test_try_to_reduce(b1: Box, b2: Box, b3: Box):
#     assert
