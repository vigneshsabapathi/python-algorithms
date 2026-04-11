"""
Heap's Algorithm — Generate All Permutations (Recursive)

Generates all n! permutations of a list by swapping elements.
Only one swap per permutation — minimizes element movement.

Time: O(n!)   Space: O(n) call stack

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/heaps_algorithm.py
"""

from __future__ import annotations


def heaps_algorithm(arr: list) -> list[list]:
    """
    Generate all permutations using Heap's algorithm (recursive).

    >>> heaps_algorithm([1, 2, 3])
    [[1, 2, 3], [2, 1, 3], [3, 1, 2], [1, 3, 2], [2, 3, 1], [3, 2, 1]]
    >>> heaps_algorithm([1])
    [[1]]
    >>> heaps_algorithm([])
    [[]]
    """
    if not arr:
        return [[]]
    result: list[list] = []
    _generate(len(arr), arr, result)
    return result


def _generate(k: int, arr: list, result: list[list]) -> None:
    if k == 1:
        result.append(arr[:])
        return

    _generate(k - 1, arr, result)

    for i in range(k - 1):
        if k % 2 == 0:
            arr[i], arr[k - 1] = arr[k - 1], arr[i]
        else:
            arr[0], arr[k - 1] = arr[k - 1], arr[0]
        _generate(k - 1, arr, result)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
