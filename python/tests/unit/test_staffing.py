"""
Unit tests for staffing.py module.
"""
import pytest

from staffing import (
    TimeUnit,
    add_shrinkage,
    calc_average_speed_of_answer,
    calc_immediate_answer,
    calc_occupancy,
    calc_service_level,
    calc_traffic_intensity,
    calc_wait_probability,
    optimise_occupancy,
    __find_min_max_agents
)


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


def test_calc_immediate_answer():
    assert calc_immediate_answer(0.321) == 0.679


def test_calc_service_level():
    assert round(calc_service_level(123, 130, 0.4244, 20, 300), 4) == 0.7339
    assert round(calc_service_level(123, 130, 1, 0, 300), 4) == 0
    assert round(calc_service_level(123, 130, 0, 1, 300), 4) == 1


def test_occupancy():
    assert round(calc_occupancy(123, 130), 3) == 0.946


def test_optimise_occupancy():
    agents, occ = optimise_occupancy(123, 130, 0.85)
    assert agents == 145
    assert round(occ, 4) == 0.8483

    agents, occ = optimise_occupancy(109, 130, 0.85)
    assert agents == 130
    assert round(occ, 4) == 0.8385


def test_calc_average_speed_of_answer():
    assert round(calc_average_speed_of_answer(123, 130, 0.4244, 300), 2) == 18.19


def test_add_shrinkage():
    assert add_shrinkage(10, 0.3) == 15
    assert add_shrinkage(11, 0.3) == 16


def test___find_min_max_agents():
    assert __find_min_max_agents(100, 300, 20, 0.8) == (8, 16)
