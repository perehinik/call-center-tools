"""
Unit tests for staffing.py module.
"""
import pytest

from staffing import calc_traffic_intensity, TimeUnit


@pytest.mark.parametrize("calls, aht, aht_unit, expected",
                         [(100, 72, TimeUnit.SEC, 2),
                          (100, 1.2, TimeUnit.MIN, 2),
                          (100, 0.5, TimeUnit.HOUR, 50)])
def test_calc_traffic_intensity(calls, aht, aht_unit, expected):
    assert calc_traffic_intensity(calls, aht, aht_unit) == expected


def test_calc_traffic_intensity_no_unit():
    assert calc_traffic_intensity(100, 72) == 2