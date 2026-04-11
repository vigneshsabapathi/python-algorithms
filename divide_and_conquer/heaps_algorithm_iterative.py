"""
Heap's Algorithm — Generate All Permutations (Iterative)

Iterative version of Heap's algorithm. Uses an auxiliary counter array
instead of recursion. Same O(n!) time, O(n) space (no call stack).

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/heaps_algorithm_iterative.py
"""

from __future__ import annotations


def heaps_algorithm_iterative(arr: list) -> list[list]:
    """
    Generate all permutations using Heap's algorithm (iterative).

    >>> heaps_algorithm_iterative([1, 2, 3])
    [[1, 2, 3], [2, 1, 3], [3, 1, 2], [1, 3, 2], [2, 3, 1], [3, 2, 1]]
    >>> heaps_algorithm_iterative([1])
    [[1]]
    >>> heaps_algorithm_iterative([])
    [[]]
    """
    n = len(arr)
    if n == 0:
        return [[]]

    result: list[list] = [arr[:]]
    c = [0] * n  # counter array
    i = 0

    while i < n:
        if c[i] < i:
            if i % 2 == 0:
                arr[0], arr[i] = arr[i], arr[0]
            else:
                arr[c[i]], arr[i] = arr[i], arr[c[i]]
            result.append(arr[:])
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
