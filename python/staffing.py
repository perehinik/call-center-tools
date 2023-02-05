"""
Module contains methods for call center staffing calculation.
"""

from enum import Enum
import math


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


def calc_service_level(traffic_intensity: float,
                       number_of_agents: int,
                       wait_probability: float,
                       target_answer_time: float,
                       aht: float) -> float:
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
    """
    occ = traffic_intensity / number_of_agents
    return occ if occ <= 1 else 1
