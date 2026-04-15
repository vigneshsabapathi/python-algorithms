"""
Power Using Recursion
=====================
Compute base^exponent recursively.
"""


def power(base: float, exponent: int) -> float:
    """
    Integer exponent; supports negative exponents.

    >>> power(2, 10)
    1024
    >>> power(3, 0)
    1
    >>> power(2, -3)
    0.125
    >>> power(5, 1)
    5
    """
    if exponent == 0:
        return 1
    if exponent < 0:
        return 1 / power(base, -exponent)
    return base * power(base, exponent - 1)


def fast_power(base: float, exponent: int) -> float:
    """
    Exponentiation by squaring: O(log n) recursion depth.

    >>> fast_power(2, 10)
    1024
    >>> fast_power(3, 13)
    1594323
    >>> fast_power(2, -4)
    0.0625
    """
    if exponent == 0:
        return 1
    if exponent < 0:
        return 1 / fast_power(base, -exponent)
    half = fast_power(base, exponent // 2)
    return half * half if exponent % 2 == 0 else half * half * base


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(power(2, 10), fast_power(2, 10))
    print(power(3, 5), fast_power(3, 5))
