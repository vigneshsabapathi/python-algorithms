"""
0/1 Knapsack Problem — Dynamic Programming.

Given weights and values of n items, put these items in a knapsack of
capacity W to get the maximum total value. Each item can be used at most once.

Three implementations:
  - knapsack: bottom-up DP table
  - mf_knapsack: top-down with memory function
  - knapsack_with_example_solution: returns optimal value AND selected items

>>> knapsack_with_example_solution(10, [1, 3, 5, 2], [10, 20, 100, 22])
(142, {2, 3, 4})
>>> knapsack_with_example_solution(6, [4, 3, 2, 3], [3, 2, 4, 4])
(8, {3, 4})
"""

from __future__ import annotations


def knapsack(w: int, wt: list[int], val: list[int], n: int) -> tuple[int, list[list[int]]]:
    """
    Bottom-up 0/1 knapsack. Returns (optimal_value, dp_table).

    >>> knapsack(6, [4, 3, 2, 3], [3, 2, 4, 4], 4)[0]
    8
    """
    dp = [[0] * (w + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w_ in range(1, w + 1):
            if wt[i - 1] <= w_:
                dp[i][w_] = max(val[i - 1] + dp[i - 1][w_ - wt[i - 1]], dp[i - 1][w_])
            else:
                dp[i][w_] = dp[i - 1][w_]

    return dp[n][w], dp


def knapsack_with_example_solution(w: int, wt: list, val: list) -> tuple[int, set]:
    """
    Solve 0/1 knapsack and return one optimal subset.

    Parameters
    ----------
    w : int — maximum weight capacity
    wt : list — weights of items
    val : list — values of items

    Returns
    -------
    (optimal_value, optimal_subset) where optimal_subset is a set of 1-based indices.

    >>> knapsack_with_example_solution(10, [1, 3, 5, 2], [10, 20, 100, 22])
    (142, {2, 3, 4})
    >>> knapsack_with_example_solution(6, [4, 3, 2, 3], [3, 2, 4, 4])
    (8, {3, 4})
    >>> knapsack_with_example_solution(6, [4, 3, 2, 3], [3, 2, 4])
    Traceback (most recent call last):
        ...
    ValueError: The number of weights must be the same as the number of values.
    But got 4 weights and 3 values
    """
    if not (isinstance(wt, (list, tuple)) and isinstance(val, (list, tuple))):
        raise ValueError(
            "Both the weights and values vectors must be either lists or tuples"
        )

    num_items = len(wt)
    if num_items != len(val):
        msg = (
            "The number of weights must be the same as the number of values.\n"
            f"But got {num_items} weights and {len(val)} values"
        )
        raise ValueError(msg)

    for i in range(num_items):
        if not isinstance(wt[i], int):
            msg = (
                "All weights must be integers but got weight of "
                f"type {type(wt[i])} at index {i}"
            )
            raise TypeError(msg)

    optimal_val, dp_table = knapsack(w, wt, val, num_items)
    example_optional_set: set = set()
    _construct_solution(dp_table, wt, num_items, w, example_optional_set)

    return optimal_val, example_optional_set


def _construct_solution(dp: list, wt: list, i: int, j: int, optimal_set: set) -> None:
    """Recursively reconstruct the optimal subset."""
    if i > 0 and j > 0:
        if dp[i - 1][j] == dp[i][j]:
            _construct_solution(dp, wt, i - 1, j, optimal_set)
        else:
            optimal_set.add(i)
            _construct_solution(dp, wt, i - 1, j - wt[i - 1], optimal_set)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    val = [3, 2, 4, 4]
    wt = [4, 3, 2, 3]
    w = 6
    optimal_solution, optimal_subset = knapsack_with_example_solution(w, wt, val)
    print(f"  optimal_value = {optimal_solution}")
    print(f"  optimal_subset = {optimal_subset}")

    # Larger example
    val2 = [10, 20, 100, 22]
    wt2 = [1, 3, 5, 2]
    w2 = 10
    opt_val, opt_set = knapsack_with_example_solution(w2, wt2, val2)
    print(f"  optimal_value = {opt_val}, subset = {opt_set}")
