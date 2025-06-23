import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app import distance_km


def test_distance_zero():
    assert distance_km((0, 0), (0, 0)) == 0


def test_distance_nonzero():
    d = distance_km((0, 0), (0, 1))
    assert d > 100 and d < 120  # approx distance between longitudes at equator
