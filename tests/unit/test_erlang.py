"""
Unit tests for erlang.py module.
"""

import pytest

from erlang import erlang_b, erlang_c


def test_erlang_b():
    assert round(erlang_b(123, 132), 4) == 0.0312


@pytest.mark.parametrize(
    "traffic_intensity, number_of_agents, expected",
    [(1, 1, 1), (123, 132, 0.3211), (12345, 12421, 0.3812), (1000, 900, 1)],
)
def test_erlang_c(traffic_intensity, number_of_agents, expected):
    wait_probability = erlang_c(traffic_intensity, number_of_agents)
    assert round(wait_probability, 4) == expected
