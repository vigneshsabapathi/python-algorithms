# Fractional Knapsack — Greedy Approach
# Source: https://github.com/TheAlgorithms/Python/blob/master/knapsack/greedy_knapsack.py

"""
A shopkeeper has bags of wheat that each have different weights and different profits.
eg.
profit 5 8 7 1 12 3 4
weight 2 7 1 6  4 2 5
max_weight 100

Constraints:
max_weight > 0
profit[i] >= 0
weight[i] >= 0

Calculate the maximum profit that the shopkeeper can make given maximum weight that can
be carried.  In the fractional variant items can be broken — take a fraction of a bag.
"""


def calc_profit(profit: list, weight: list, max_weight: int) -> float:
    """
    Greedy fractional knapsack: sort items by profit/weight ratio descending,
    take whole items when possible, fractional when necessary.

    :param profit: List of profits for each item
    :param weight: List of weights for each item
    :param max_weight: Maximum weight capacity
    :return: Maximum expected gain (float because of fractional items)

    >>> calc_profit([1, 2, 3], [3, 4, 5], 15)
    6
    >>> calc_profit([10, 9, 8], [3, 4, 5], 25)
    27
    >>> calc_profit([5, 8, 7, 1, 12, 3, 4], [2, 7, 1, 6, 4, 2, 5], 100)
    40
    >>> calc_profit([5, 8, 7, 1, 12, 3, 4], [2, 7, 1, 6, 4, 2, 5], 10)
    28.142857142857142
    >>> calc_profit([60, 100, 120], [10, 20, 30], 50)
    240
    >>> calc_profit([], [], 50)
    0
    >>> calc_profit([10], [5], 0)
    Traceback (most recent call last):
        ...
    ValueError: max_weight must be greater than zero.
    >>> calc_profit([10], [5, 3], 20)
    Traceback (most recent call last):
        ...
    ValueError: The length of profit and weight must be same.
    >>> calc_profit([-1], [5], 20)
    Traceback (most recent call last):
        ...
    ValueError: Profit can not be negative.
    >>> calc_profit([10], [-5], 20)
    Traceback (most recent call last):
        ...
    ValueError: Weight can not be negative.
    """
    if len(profit) != len(weight):
        raise ValueError("The length of profit and weight must be same.")
    if max_weight <= 0:
        raise ValueError("max_weight must be greater than zero.")
    if any(p < 0 for p in profit):
        raise ValueError("Profit can not be negative.")
    if any(w < 0 for w in weight):
        raise ValueError("Weight can not be negative.")

    if not profit:
        return 0

    # Build (profit/weight ratio, profit, weight) tuples and sort descending by ratio
    items = sorted(
        zip(profit, weight),
        key=lambda x: x[0] / x[1] if x[1] > 0 else float("inf"),
        reverse=True,
    )

    remaining = max_weight
    gain = 0.0

    for p, w in items:
        if remaining <= 0:
            break
        if w <= remaining:
            # Take the whole item
            gain += p
            remaining -= w
        else:
            # Take a fraction of the item
            gain += (remaining / w) * p
            remaining = 0

    return gain if gain != int(gain) else int(gain)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
