"""
Greedy Algorithm — Coin change / minimum coins problem.

Find the minimum number of coins needed to make a given amount,
using a greedy approach (works optimally for standard denominations).

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/greedy.py
"""

from __future__ import annotations


def greedy_coin_change(
    denominations: list[int], amount: int
) -> list[int]:
    """
    Find coins needed to make the amount using greedy approach.

    Returns list of coins used (may not be optimal for arbitrary denominations).

    >>> greedy_coin_change([25, 10, 5, 1], 41)
    [25, 10, 5, 1]
    >>> greedy_coin_change([25, 10, 5, 1], 0)
    []
    >>> greedy_coin_change([25, 10, 5, 1], 30)
    [25, 5]
    >>> greedy_coin_change([1], 5)
    [1, 1, 1, 1, 1]
    >>> greedy_coin_change([25, 10, 5, 1], 100)
    [25, 25, 25, 25]
    """
    coins_used: list[int] = []
    denominations_sorted = sorted(denominations, reverse=True)

    remaining = amount
    for coin in denominations_sorted:
        while remaining >= coin:
            coins_used.append(coin)
            remaining -= coin

    return coins_used


def greedy_fractional_knapsack(
    items: list[tuple[int, int]], capacity: int
) -> float:
    """
    Fractional knapsack using greedy approach.

    Each item is (value, weight). Returns maximum value achievable.

    >>> greedy_fractional_knapsack([(60, 10), (100, 20), (120, 30)], 50)
    240.0
    >>> greedy_fractional_knapsack([(60, 10)], 5)
    30.0
    >>> greedy_fractional_knapsack([], 50)
    0.0
    >>> greedy_fractional_knapsack([(100, 20)], 0)
    0.0
    """
    if not items or capacity <= 0:
        return 0.0

    # Sort by value-to-weight ratio in decreasing order
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0.0
    remaining_capacity = capacity

    for value, weight in sorted_items:
        if remaining_capacity <= 0:
            break
        if weight <= remaining_capacity:
            total_value += value
            remaining_capacity -= weight
        else:
            # Take fraction
            total_value += value * (remaining_capacity / weight)
            remaining_capacity = 0

    return total_value


if __name__ == "__main__":
    import doctest

    doctest.testmod()
