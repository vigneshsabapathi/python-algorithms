"""
Longest Increasing Subsequence — Iterative DP approach.

O(n^2) time, O(n) space. Builds the actual subsequence, not just the length.

>>> longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80])
[10, 22, 33, 50, 60, 80]
>>> longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9])
[1, 2, 3, 9]
>>> longest_subsequence([9, 8, 7, 6, 5, 7])
[7, 7]
>>> longest_subsequence([1, 1, 1])
[1, 1, 1]
>>> longest_subsequence([])
[]
"""

from __future__ import annotations

import copy


def longest_subsequence(array: list[int]) -> list[int]:
    """
    Find the longest non-decreasing subsequence using iterative DP.

    For each position i, stores the actual best subsequence ending at i.

    >>> longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80])
    [10, 22, 33, 50, 60, 80]
    >>> longest_subsequence([28, 26, 12, 23, 35, 39])
    [12, 23, 35, 39]
    >>> longest_subsequence([])
    []
    """
    n = len(array)
    longest_increasing_subsequence: list[list[int]] = []
    for i in range(n):
        longest_increasing_subsequence.append([array[i]])

    for i in range(1, n):
        for prev in range(i):
            if array[prev] <= array[i] and len(
                longest_increasing_subsequence[prev]
            ) + 1 > len(longest_increasing_subsequence[i]):
                longest_increasing_subsequence[i] = copy.copy(
                    longest_increasing_subsequence[prev]
                )
                longest_increasing_subsequence[i].append(array[i])

    result: list[int] = []
    for i in range(n):
        if len(longest_increasing_subsequence[i]) > len(result):
            result = longest_increasing_subsequence[i]

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = [
        [10, 22, 9, 33, 21, 50, 41, 60, 80],
        [4, 8, 7, 5, 1, 12, 2, 3, 9],
        [9, 8, 7, 6, 5, 7],
        [1, 2, 3, 4, 5],
    ]
    for arr in tests:
        print(f"  LIS_iterative({arr}) = {longest_subsequence(arr)}")
