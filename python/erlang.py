"""
Module contains implementation of Erlang B, C formulas.
"""


def calc_wait_probability(t_intensity: float, agents: int) -> float:
    """
    Calculates wait probability using Erlang C formula.

    Method uses fast algorithm to avoid dealing with factorials, power and big numbers.
    Result of calculations is same as for Erlang C formula.

    Parameters
    ----------
    t_intensity : float
        Traffic intensity in Erlangs. Can be calculated using method calc_traffic_intensity().
    agents : int
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
    if agents <= t_intensity:
        return 1
    product = 1
    result = 0
    for i in range(0, agents):
        product = product * ((agents - i) / t_intensity)
        result += product
    result = 1 / (result * (agents - t_intensity) / agents + 1)
    return result if result <= 1 else 1
