"""
Module contains implementation of Erlang B, C formulas.
"""


def erlang_b(t_intensity: float, agents: int) -> float:
    """
    Calculates blocking probability using Erlang B formula.

    Returns probability that all agents are busy.
    Method uses fast algorithm to avoid dealing with factorials, power and big numbers.
    Result of calculations is same as for original Erlang B formula.

    Parameters
    ----------
    t_intensity : float
        Traffic intensity in Erlangs.
    agents : int
        Number of agents.

    Returns
    -------
    float
        Probability of blocking. Range 0-1(0%-100%).

    Examples
    --------
    >>> erlang_b(123, 132)
    0.0346
    """
    result = 1
    for i in range(1, agents + 1):
        result = 1 + result * i / t_intensity
    return 1 / result


def erlang_c(t_intensity: float, agents: int) -> float:
    """
    Calculates wait probability using Erlang C formula.

    Method uses fast algorithm to avoid dealing with factorials, power and big numbers.
    Result of calculations is same as for Erlang C formula.

    Parameters
    ----------
    t_intensity : float
        Traffic intensity in Erlangs.
    agents : int
        Number of agents.

    Returns
    -------
    float
        Probability that there is no available agents to answer the call. Range 0-1(0%-100%).

    Examples
    --------
    >>> erlang_c(123, 132)
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
