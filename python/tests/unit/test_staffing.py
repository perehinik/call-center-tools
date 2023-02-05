"""
Unit tests for staffing.py module.
"""
import pytest

from staffing import TimeUnit, calc_traffic_intensity, calc_wait_probability, calc_service_level


@pytest.mark.parametrize(
    "calls, aht, aht_unit, expected",
    [(100, 72, TimeUnit.SEC, 2), (100, 1.2, TimeUnit.MIN, 2), (100, 0.5, TimeUnit.HOUR, 50)],
)
def test_calc_traffic_intensity(calls, aht, aht_unit, expected):
    assert calc_traffic_intensity(calls, aht, aht_unit) == expected


def test_calc_traffic_intensity_no_unit():
    assert calc_traffic_intensity(100, 72) == 2


@pytest.mark.parametrize(
    "traffic_intensity, number_of_agents, expected",
    [(1, 1, 1), (123, 132, 0.3211), (12345, 12421, 0.3812), (1000, 900, 1)],
)
def test_calc_wait_probability(traffic_intensity, number_of_agents, expected):
    wait_probability = calc_wait_probability(traffic_intensity, number_of_agents)
    assert round(wait_probability, 4) == expected


def test_calc_service_level():
    assert round(calc_service_level(123, 130, 0.4244, 20, 300), 4) == 0.7339
    assert round(calc_service_level(123, 130, 1, 0, 300), 4) == 0
    assert round(calc_service_level(123, 130, 0, 1, 300), 4) == 1
