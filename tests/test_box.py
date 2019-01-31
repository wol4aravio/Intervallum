import pytest
from numpy.testing import assert_almost_equal

from intervallum.interval import Interval
from intervallum.box import Box


@pytest.fixture(scope="session")
def b1() -> Box:
    return Box(1.0, Interval(2.0, 3.0), Interval(4.0, 7.0), 9)


def test_base(b1: Box):
    assert_almost_equal(b1[0], 1.0)
    assert b1[1] == Interval(2.0, 3.0)
