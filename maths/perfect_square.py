"""
Perfect Square
==============
A perfect square is an integer that is the square of another integer.
"""
import math


def perfect_square(n: int) -> bool:
    """
    Return True if ``n`` is a non-negative perfect square.

    >>> perfect_square(0)
    True
    >>> perfect_square(1)
    True
    >>> perfect_square(9)
    True
    >>> perfect_square(16)
    True
    >>> perfect_square(15)
    False
    >>> perfect_square(-4)
    False
    """
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def perfect_square_binary_search(n: int) -> bool:
    """
    >>> perfect_square_binary_search(25)
    True
    >>> perfect_square_binary_search(26)
    False
    """
    if n < 0:
        return False
    lo, hi = 0, n
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == n:
            return True
        if sq < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for x in (0, 1, 4, 9, 15, 16, 100, 9999, 10000):
        print(f"{x}: {perfect_square(x)}")
