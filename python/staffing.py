from enum import Enum

"""
Module contains methods for call center staffing calculation.
"""


class TimeUnit(Enum):
    """
    Contains time units and corresponding conversion divisor to convert value to hours.
    """
    SEC = 3600
    MIN = 60
    HOUR = 1


def calc_traffic_intensity(calls_per_hour: float, aht: float, aht_unit: TimeUnit = TimeUnit.SEC) -> float:
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
        Probability that there is no available agents to answer the call. can be 0-1.
    """
    product = 1
    result = 0
    for i in range(0, number_of_agents):
        product = product * ((number_of_agents - i) / traffic_intensity)
        result += product
    result = result * ((number_of_agents - traffic_intensity) / number_of_agents) + 1
    result = 1 / result
    return result if result <= 1 else 1
