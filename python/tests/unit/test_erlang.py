"""
Unit tests for erlang.py module.
"""

import pytest

from staffing import (
    calc_wait_probability,
)


@pytest.mark.parametrize(
    "traffic_intensity, number_of_agents, expected",
    [(1, 1, 1), (123, 132, 0.3211), (12345, 12421, 0.3812), (1000, 900, 1)],
)
def test_calc_wait_probability(traffic_intensity, number_of_agents, expected):
    wait_probability = calc_wait_probability(traffic_intensity, number_of_agents)
    assert round(wait_probability, 4) == expected
