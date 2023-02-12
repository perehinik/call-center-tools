"""
Unit tests for staffing.py module.
"""


from staffing import (
    optimise_occupancy,
    __find_min_max_agents
)


def test_optimise_occupancy():
    agents, occ = optimise_occupancy(123, 130, 0.85)
    assert agents == 145
    assert round(occ, 4) == 0.8483

    agents, occ = optimise_occupancy(109, 130, 0.85)
    assert agents == 130
    assert round(occ, 4) == 0.8385


def test___find_min_max_agents():
    assert __find_min_max_agents(100, 300, 20, 0.8) == (8, 16)

