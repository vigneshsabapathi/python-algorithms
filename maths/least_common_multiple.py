"""
LCM(a, b) = |a*b| / gcd(a, b). Extends to n numbers by reduction.

>>> lcm(4, 6)
12
>>> lcm(7, 5)
35
>>> lcm_of_n([4, 6, 8])
24
>>> lcm_of_n([3, 5, 7])
105
"""

from functools import reduce
from math import gcd


def lcm(a: int, b: int) -> int:
    """LCM of two integers."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def lcm_of_n(nums: list[int]) -> int:
    """LCM of a list."""
    return reduce(lcm, nums)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(lcm_of_n([4, 6, 8]))
