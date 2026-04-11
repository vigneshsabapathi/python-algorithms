# 0/1 Knapsack — Naive Recursive Approach
# Source: https://github.com/TheAlgorithms/Python/blob/master/knapsack/recursive_approach_knapsack.py

"""
A shopkeeper has bags of wheat that each have different weights and different profits.
For each item, decide to include or exclude it (0/1 choice).
Find the maximum profit within the weight limit using pure recursion.

This explores the full binary decision tree — O(2^n) time.
"""


def knapsack(
    weights: list, values: list, number_of_items: int, max_weight: int, index: int
) -> int:
    """
    Recursive 0/1 knapsack — brute-force all subsets.

    :param weights: List of item weights
    :param values: List of item values (profits)
    :param number_of_items: Total number of items available
    :param max_weight: Maximum weight capacity
    :param index: Current item index being considered
    :return: Maximum expected gain

    >>> knapsack([1, 2, 4, 5], [5, 4, 8, 6], 4, 5, 0)
    13
    >>> knapsack([3, 4, 5], [10, 9, 8], 3, 25, 0)
    27
    >>> knapsack([10, 20, 30], [60, 100, 120], 3, 50, 0)
    220
    >>> knapsack([1, 2, 3], [6, 10, 12], 3, 5, 0)
    22
    >>> knapsack([1, 3, 4, 5], [1, 4, 5, 7], 4, 7, 0)
    9
    >>> knapsack([], [], 0, 10, 0)
    0
    """
    # Base case: no items left to consider
    if index == number_of_items:
        return 0

    # Option 1: skip current item
    exclude = knapsack(weights, values, number_of_items, max_weight, index + 1)

    # Option 2: include current item (if it fits)
    include = 0
    if weights[index] <= max_weight:
        include = values[index] + knapsack(
            weights, values, number_of_items, max_weight - weights[index], index + 1
        )

    return max(exclude, include)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
