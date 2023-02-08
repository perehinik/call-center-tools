"""
Module contains methods for call center staffing calculation.
"""

import math
from enum import Enum
from typing import Tuple, Dict, Optional
from dataclasses import dataclass


class TimeUnit(Enum):
    """
    Contains time units and corresponding conversion divisor to convert value to hours.
    """

    SEC = 3600
    MIN = 60
    HOUR = 1


def calc_traffic_intensity(
    calls_per_hour: float, aht: float, aht_unit: TimeUnit = TimeUnit.SEC
) -> float:
    """
    Calculates traffic intensity in Erlangs.

    Parameters
    ----------
    calls_per_hour : float
        Number of calls offered per hour.
    aht : float
        Average Handling Time. Default unit is seconds.
    aht_unit : TimeUnit, default = TimeUnit.SEC
        Unit for average handling time.

    Returns
    -------
    float
        Traffic intensity in Erlangs.

    Examples
    --------
    >>> calc_traffic_intensity(100, 72)
    2
    >>> calc_traffic_intensity(100, 1.2, TimeUnit.MIN)
    2
    """
    return calls_per_hour * (aht / aht_unit.value)


def calc_wait_probability(traffic_intensity: float, number_of_agents: int) -> float:
    """
    Calculates wait probability using Erlang C formula.

    Method uses fast algorithm to avoid dealing with factorials, power and big numbers.
    Result of calculations is same as for Erlang C formula.

    Parameters
    ----------
    traffic_intensity : float
        Traffic intensity in Erlangs. Can be calculated using method calc_traffic_intensity().
    number_of_agents : int
        Number of agents.

    Returns
    -------
    float
        Probability that there is no available agents to answer the call. Range 0-1(0%-100%).

    Examples
    --------
    >>> calc_wait_probability(123, 132)
    0.3211161792617074
    """
    product = 1
    result = 0
    for i in range(0, number_of_agents):
        product = product * ((number_of_agents - i) / traffic_intensity)
        result += product
    result = result * ((number_of_agents - traffic_intensity) / number_of_agents) + 1
    result = 1 / result
    return result if result <= 1 else 1


def calc_immediate_answer(wait_probability: float) -> float:
    """
    Calculates amount of calls answered immediately.

    Parameters
    ----------
    wait_probability : float
        Probability that there is no available agents to answer the call. Should be 0-1.

    Returns
    -------
    float
        Amount of calls answered immediately. Range 0-1(0%-100%).

    Examples
    --------
    >>> calc_immediate_answer(0.321)
    0.679
    """
    return 1 - wait_probability


def calc_service_level(
    traffic_intensity: float,
    number_of_agents: int,
    wait_probability: float,
    target_answer_time: float,
    aht: float,
) -> float:
    """
    Calculates how many calls will be answered in target time.

    Parameters
    ----------
    traffic_intensity : float
        Traffic intensity in Erlangs. Can be calculated using method calc_traffic_intensity().
    number_of_agents : int
        Number of agents.
    wait_probability : float
        Probability that there is no available agents to answer the call. Should be 0-1.
    target_answer_time : float
        Target time of answer to incoming call. Should have same unit as aht.
    aht : float
        Average Handling Time. Should have same unit as target_answer_time.

    Returns
    -------
    float
         Service level - amount of calls answered in target time. Range 0-1(0%-100%).

    Examples
    --------
    >>> calc_service_level(123, 130, 0.4244, 20, 300)
    0.733863392210115
    """
    expon = -abs((number_of_agents - traffic_intensity) * target_answer_time / aht)
    return 1 - abs(wait_probability * pow(math.e, expon))


def calc_occupancy(traffic_intensity: float, number_of_agents: int) -> float:
    """
    Calculate how much time agents spend talking with customers.

    Parameters
    ----------
    traffic_intensity : float
        Traffic intensity in Erlangs. Can be calculated using method calc_traffic_intensity().
    number_of_agents : int
        Number of agents.

    Returns
    -------
    float
        Occupancy. Range 0-1(0%-100%).

    Examples
    --------
    >>> calc_occupancy(123, 130)
    0.9461538461538461
    """
    occ = traffic_intensity / number_of_agents
    return occ if occ <= 1 else 1


def optimise_occupancy(
    traffic_intensity: float, number_of_agents: int, occupancy_target: float
) -> Tuple[int, float]:
    """
    Calculate number of agents to meet occupancy target.

    Parameters
    ----------
    traffic_intensity : float
        Traffic intensity in Erlangs. Can be calculated using method calc_traffic_intensity().
    number_of_agents : int
        Number of agents.
    occupancy_target : float
        The highest allowed occupancy. Should be 0-1.

    Returns
    -------
    Tuple [int, float]
        (Number of agents, optimised occupancy)

    Examples
    --------
    >>> optimise_occupancy(123, 130, 0.85)
    (145, 0.8482758620689655)
    """
    occ = calc_occupancy(traffic_intensity, number_of_agents)
    if occ <= occupancy_target:
        return number_of_agents, occ
    optimised_occ_agents = math.ceil(traffic_intensity / occupancy_target)
    occ = calc_occupancy(traffic_intensity, optimised_occ_agents)
    return optimised_occ_agents, occ


def calc_average_speed_of_answer(
    traffic_intensity: float, number_of_agents: int, wait_probability: float, aht: float
) -> float:
    """
    Calculates average time in which call is answered.

    Parameters
    ----------
    traffic_intensity : float
        Traffic intensity in Erlangs. Can be calculated using method calc_traffic_intensity().
    number_of_agents : int
        Number of agents.
    wait_probability : float
        Probability that there is no available agents to answer the call. Should be 0-1.
    aht : float
        Average Handling Time.

    Returns
    -------
    float
        Average time in which call is answered. Unit is the same as for AHT.

    Examples
    --------
    >>> calc_average_speed_of_answer(123, 130, 0.4244, 300)
    0.9461538461538461
    """
    return (wait_probability * aht) / (number_of_agents - traffic_intensity)


def add_shrinkage(number_of_agents: int, shrinkage: float) -> int:
    """
    Calculates amount of agents with shrinkage applied.

    Parameters
    ----------
    number_of_agents : int
        Number of agents.
    shrinkage : float
        Percentage of time when agents are not answering calls. Should be 0-1.

    Returns
    -------
    int
        Number of agents with applied shrinkage.

    Exapmles
    --------
    >>> add_shrinkage(10, 0.3)
    15
    """
    return math.ceil(number_of_agents / (1 - shrinkage))


@dataclass
class StaffingData:
    traffic_intensity: float
    wait_probability: float
    immediate_answer: float
    average_speed_of_answer: float
    occupancy: float
    agents: int
    agents_with_shrinkage: int


def __find_min_max_agents(
    number_of_agents: int,
    calls_per_hour: float,
    aht: float,
    target_answer_time: float,
    aht_unit: TimeUnit = TimeUnit.SEC
) -> Tuple[int, Dict[StaffingData]]:
    """
    Find min and max number of agents for binary search.

    Parameters
    ----------
    number_of_agents : int
        Number of agents.
    calls_per_hour : float
        Number of calls offered per hour.
    aht : float
        Average Handling Time. Default unit is seconds.
    target_answer_time : float
        Target time of answer to incoming call. Should have same unit as aht.
    aht_unit : TimeUnit, default = TimeUnit.SEC
        Unit for average handling time.

    Returns
    -------
    Tuple[int, int, Dict[int, StaffingData]]
        Tuple of max number of agents and dictionary with calculated data.
    """
    pass


def __calc_all(
    number_of_agents: int,
    calls_per_hour: float,
    aht: float,
    target_answer_time: float,
    shrinkage: Optional[float] = None,
    aht_unit: TimeUnit = TimeUnit.SEC
) -> StaffingData:
    """
    Calculate all parameters for specified number of agents.

    Parameters
    ----------
    number_of_agents : int
        Number of agents.
    calls_per_hour : float
        Number of calls offered per hour.
    aht : float
        Average Handling Time. Default unit is seconds.
    target_answer_time : float
        Target time of answer to incoming call. Should have same unit as aht.
    shrinkage : float, optional
        Percentage of time agents are paid for but don't answer for calls.
        For example meetings, trainings, etc.. Should be 0-1 (0-100%).
    aht_unit : TimeUnit, default = TimeUnit.SEC
        Unit for average handling time.

    Returns
    -------
    StaffingData
        Result of calculations for specified number of agents.
    """
    pass


def calc_staffing(
    calls_per_hour: float,
    aht: float,
    number_of_agents: Optional[int] = None,
    target_occupancy: Optional[float] = None,
    target_answer_time: float = 20,
    target_service_level: float = 0.80,
    shrinkage: Optional[float] = None,
    time_unit: TimeUnit = TimeUnit.SEC
) -> StaffingData:
    """
    Automatic staffing calculations.

    If agents number specified - calculates only for this number of agents.
    else - automatic adjusting of number of agents to achieve the best parameters.

    Parameters
    ----------
    calls_per_hour : float
        Number of calls offered per hour.
    aht : float
        Average Handling Time. Default unit is seconds.
    number_of_agents : int, optional.
        Number of agents. If not specified
    target_occupancy : float, optional
        If specified - algorithm may increase required number of agents to achieve lower occupancy.
    target_answer_time : float, default 20
        Target time of answer to incoming call. Should have same time unit as aht.
    target_service_level : float, default 0.80 (80%).
        Percentage of calls that should be answered in target_answer_time.
    shrinkage : float, optional
        Percentage of time agents are paid for but don't answer for calls.
        For example meetings, trainings, etc.. Should be 0-1 (0-100%).
    time_unit : TimeUnit, default = TimeUnit.SEC
        Unit for average handling time and target_answer_time.

    Returns
    -------
    StaffingData
        Result of calculations.
    """
    pass
