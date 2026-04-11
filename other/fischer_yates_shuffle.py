"""
Fischer-Yates Shuffle — Unbiased in-place random permutation.

The modern version (Knuth shuffle) iterates from the end, swapping each element
with a randomly chosen element from the remaining unshuffled portion.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/fischer_yates_shuffle.py
"""

from __future__ import annotations

import random


def fischer_yates_shuffle(data: list, rng: random.Random | None = None) -> list:
    """
    Shuffle a list in-place using the Fischer-Yates algorithm.

    Returns the list for convenience (same reference, modified in-place).

    >>> rng = random.Random(42)
    >>> fischer_yates_shuffle([1, 2, 3, 4, 5], rng)
    [4, 2, 3, 5, 1]
    >>> fischer_yates_shuffle([], rng)
    []
    >>> fischer_yates_shuffle([1], rng)
    [1]
    >>> result = fischer_yates_shuffle([1, 2, 3, 4, 5], random.Random(0))
    >>> sorted(result) == [1, 2, 3, 4, 5]
    True
    """
    if rng is None:
        rng = random.Random()

    n = len(data)
    for i in range(n - 1, 0, -1):
        j = rng.randint(0, i)
        data[i], data[j] = data[j], data[i]

    return data


if __name__ == "__main__":
    import doctest

    doctest.testmod()
