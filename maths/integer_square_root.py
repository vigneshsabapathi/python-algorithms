"""
Integer square root: largest k such that k*k <= n.

>>> isqrt(0)
0
>>> isqrt(1)
1
>>> isqrt(2)
1
>>> isqrt(16)
4
>>> isqrt(17)
4
>>> isqrt(10**18)
1000000000
"""


def isqrt(n: int) -> int:
    """Newton's method integer square root.

    >>> isqrt(100)
    10
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n < 2:
        return n
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(isqrt(100), isqrt(10**18))
