"""
Integration tests for staffing.py module.
"""


from staffing import __find_min_max_agents, calc_staffing


def test___find_min_max_agents():
    assert __find_min_max_agents(8, 300, 20, 0.8) == (8, 16)


def test_calc_staffing():
    result = calc_staffing(
        calls_per_hour=1000,
        aht=120,
        max_occupancy=0.85,
        target_answer_time=20,
        target_service_level=0.8,
        shrinkage=0.3,
    )

    assert result.agents == 40
    assert round(result.traffic_intensity, 0) == 33
    assert round(result.wait_probability, 2) == 0.19
    assert round(result.immediate_answer, 2) == 0.81
    assert round(result.service_level, 2) == 0.94
    assert round(result.average_speed_of_answer, 1) == 3.4
    assert round(result.occupancy, 2) == 0.83
    assert result.agents_with_shrinkage == 58


def test_calc_staffing_with_agents():
    result = calc_staffing(
        calls_per_hour=1000,
        aht=120,
        agents=35,
        max_occupancy=0.85,
        target_answer_time=20,
        target_service_level=0.8,
        shrinkage=0.3,
    )

    assert result.agents == 35
    assert round(result.traffic_intensity, 0) == 33
    assert round(result.wait_probability, 1) == 0.7
    assert round(result.immediate_answer, 1) == 0.3
    assert round(result.service_level, 2) == 0.47
    assert round(result.average_speed_of_answer, 2) == 50.15
    assert round(result.occupancy, 2) == 0.95
    assert result.agents_with_shrinkage == 50
