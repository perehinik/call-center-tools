"""
Unit tests for staffing.py module.
"""


from staffing import __find_min_max_agents


def test___find_min_max_agents():
    assert __find_min_max_agents(8, 300, 20, 0.8) == (8, 16)
