"""
Matrix Chain Multiplication — Minimum number of scalar multiplications.

Given a sequence of matrices, find the most efficient way to multiply them.
The order of multiplication can drastically change the number of operations.

Example: arr = [40, 20, 30, 10, 30] represents 4 matrices:
  40x20, 20x30, 30x10, 10x30

Two approaches:
  - matrix_chain_multiply: bottom-up DP, O(n^3) time
  - matrix_chain_order: top-down with @cache

>>> matrix_chain_multiply([1, 2, 3, 4, 3])
30
>>> matrix_chain_multiply([10])
0
>>> matrix_chain_multiply([10, 20])
0
>>> matrix_chain_multiply([19, 2, 19])
722
>>> matrix_chain_order([1, 2, 3, 4, 3])
30
"""

from __future__ import annotations

from functools import cache
from sys import maxsize


def matrix_chain_multiply(arr: list[int]) -> int:
    """
    Bottom-up DP for minimum matrix chain multiplication cost.

    >>> matrix_chain_multiply([1, 2, 3, 4, 3])
    30
    >>> matrix_chain_multiply([10])
    0
    >>> matrix_chain_multiply([10, 20])
    0
    >>> matrix_chain_multiply([19, 2, 19])
    722
    """
    if len(arr) < 2:
        return 0
    n = len(arr)
    dp = [[maxsize for _ in range(n)] for _ in range(n)]

    for i in range(n - 1, 0, -1):
        for j in range(i, n):
            if i == j:
                dp[i][j] = 0
                continue
            for k in range(i, j):
                dp[i][j] = min(
                    dp[i][j], dp[i][k] + dp[k + 1][j] + arr[i - 1] * arr[k] * arr[j]
                )

    return dp[1][n - 1]


def matrix_chain_order(dims: list[int]) -> int:
    """
    Top-down (cached recursion) for minimum matrix chain multiplication cost.

    >>> matrix_chain_order([1, 2, 3, 4, 3])
    30
    >>> matrix_chain_order([10])
    0
    >>> matrix_chain_order([10, 20])
    0
    >>> matrix_chain_order([19, 2, 19])
    722
    """

    @cache
    def a(i: int, j: int) -> int:
        return min(
            (a(i, k) + dims[i] * dims[k] * dims[j] + a(k, j) for k in range(i + 1, j)),
            default=0,
        )

    return a(0, len(dims) - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = [
        [1, 2, 3, 4, 3],
        [40, 20, 30, 10, 30],
        [10, 20, 30, 40, 30],
        [19, 2, 19],
    ]
    for arr in tests:
        bu = matrix_chain_multiply(arr)
        td = matrix_chain_order(arr)
        tag = "OK" if bu == td else "FAIL"
        print(f"  [{tag}] MCM({arr}) = bottom_up:{bu}, top_down:{td}")
