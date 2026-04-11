"""
Fast Power (Exponentiation by Squaring) — Divide and Conquer

Compute x^n in O(log n) multiplications instead of O(n).

Key identity:
  x^n = (x^(n/2))^2        if n is even
  x^n = x * (x^(n/2))^2    if n is odd

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/power.py
"""

from __future__ import annotations


def power(x: int | float, n: int) -> int | float:
    """
    Compute x^n using fast exponentiation (recursive).

    >>> power(2, 10)
    1024
    >>> power(2, 0)
    1
    >>> power(3, 3)
    27
    >>> power(5, 1)
    5
    >>> power(2, -3)
    0.125
    >>> power(0, 0)
    1
    >>> power(0, 5)
    0
    >>> power(-2, 3)
    -8
    >>> power(-2, 4)
    16
    """
    if n < 0:
        return 1.0 / power(x, -n)
    if n == 0:
        return 1
    if n == 1:
        return x

    half = power(x, n // 2)
    if n % 2 == 0:
        return half * half
    else:
        return half * half * x


def power_iterative(x: int | float, n: int) -> int | float:
    """
    Compute x^n using iterative fast exponentiation.

    >>> power_iterative(2, 10)
    1024
    >>> power_iterative(2, 0)
    1
    >>> power_iterative(3, 3)
    27
    >>> power_iterative(2, -3)
    0.125
    >>> power_iterative(-2, 3)
    -8
    """
    if n < 0:
        x = 1.0 / x
        n = -n

    result = 1
    base = x
    while n > 0:
        if n % 2 == 1:
            result *= base
        base *= base
        n //= 2
    return result


def power_mod(x: int, n: int, mod: int) -> int:
    """
    Compute (x^n) % mod using fast exponentiation.
    Essential for RSA, Diffie-Hellman, competitive programming.

    >>> power_mod(2, 10, 1000)
    24
    >>> power_mod(3, 13, 7)
    3
    >>> power_mod(2, 100, 1000000007)
    976371285
    """
    if mod <= 0:
        raise ValueError("mod must be positive")
    if n < 0:
        raise ValueError("Negative exponent not supported for modular power")

    result = 1
    x = x % mod
    while n > 0:
        if n % 2 == 1:
            result = (result * x) % mod
        x = (x * x) % mod
        n //= 2
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
