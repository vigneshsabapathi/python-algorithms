"""
k-th lexicographic permutation of [0, 1, ..., n-1] (0-indexed).

Uses factorial number system: determine the position of each digit without
enumerating all permutations.

>>> kth_permutation(3, 0)
[0, 1, 2]
>>> kth_permutation(3, 5)
[2, 1, 0]
>>> kth_permutation(4, 9)
[1, 2, 3, 0]
"""

from math import factorial


def kth_permutation(n: int, k: int) -> list[int]:
    """Return the k-th (0-indexed) permutation of range(n).

    >>> kth_permutation(5, 0)
    [0, 1, 2, 3, 4]
    """
    if not 0 <= k < factorial(n):
        raise ValueError("k out of range")
    digits = list(range(n))
    result = []
    for i in range(n, 0, -1):
        f = factorial(i - 1)
        idx = k // f
        k %= f
        result.append(digits.pop(idx))
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(kth_permutation(4, 9))
