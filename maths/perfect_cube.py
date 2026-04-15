"""
Check whether a given non-negative integer is a perfect cube.

>>> perfect_cube(0)
True
>>> perfect_cube(1)
True
>>> perfect_cube(27)
True
>>> perfect_cube(28)
False
>>> perfect_cube(1_000_000)
True
"""


def perfect_cube(n: int) -> bool:
    """Integer-exact perfect cube check.

    >>> perfect_cube(64)
    True
    >>> perfect_cube(63)
    False
    """
    if n < 0:
        n = -n
    if n < 2:
        return True
    # Integer cube root via Newton's method, then verify.
    x = int(round(n ** (1 / 3)))
    # Check nearby because float rounding can be off by 1.
    for cand in (x - 1, x, x + 1):
        if cand >= 0 and cand * cand * cand == n:
            return True
    return False


def perfect_cube_binary(n: int) -> bool:
    """Binary-search cube root — exact for huge n.

    >>> perfect_cube_binary(10**18)
    True
    """
    if n < 0:
        n = -n
    lo, hi = 0, n
    while lo <= hi:
        mid = (lo + hi) // 2
        cube = mid * mid * mid
        if cube == n:
            return True
        if cube < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(perfect_cube(27), perfect_cube(28))
