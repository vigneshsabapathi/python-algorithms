# 0/1 Knapsack — Dynamic Programming (Bottom-Up Tabulation)
# Source: https://github.com/TheAlgorithms/Python/blob/master/knapsack/knapsack.py

"""
Given N items, each with a weight and value, determine the maximum value
achievable within a weight capacity W.  Each item may be used at most once
(0/1 property).

Classic DP formulation:
    dp[i][w] = max(dp[i-1][w],  dp[i-1][w - wt[i]] + val[i])  if wt[i] <= w
             = dp[i-1][w]                                       otherwise
"""

from __future__ import annotations


def knapsack(capacity: int, weights: list[int], values: list[int], n: int) -> int:
    """
    0/1 Knapsack using bottom-up DP tabulation.

    :param capacity: Maximum weight capacity of the knapsack
    :param weights: List of item weights
    :param values: List of item values
    :param n: Number of items
    :return: Maximum achievable value

    >>> knapsack(50, [10, 20, 30], [60, 100, 120], 3)
    220
    >>> knapsack(10, [5, 4, 6, 3], [10, 40, 30, 50], 4)
    90
    >>> knapsack(0, [10, 20, 30], [60, 100, 120], 3)
    0
    >>> knapsack(5, [1, 2, 3], [6, 10, 12], 3)
    22
    >>> knapsack(7, [1, 3, 4, 5], [1, 4, 5, 7], 4)
    9
    >>> knapsack(15, [1, 5, 10], [10, 50, 100], 3)
    150
    """
    # Build (n+1) x (capacity+1) table initialized to 0
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i - 1][w]
            # Take item i if it fits
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])

    return dp[n][capacity]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
