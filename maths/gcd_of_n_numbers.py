"""
GCD of n numbers using Euclidean algorithm.

>>> gcd_of_n([12, 18, 24])
6
>>> gcd_of_n([7, 14, 28])
7
>>> gcd_of_n([5])
5
>>> gcd_of_n([17, 13])
1
"""

from functools import reduce


def gcd_pair(a: int, b: int) -> int:
    """Euclidean GCD of two integers."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def gcd_of_n(nums: list[int]) -> int:
    """GCD of a list.

    >>> gcd_of_n([100, 50, 25])
    25
    """
    if not nums:
        raise ValueError("empty list")
    return reduce(gcd_pair, nums)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(gcd_of_n([12, 18, 24]))
