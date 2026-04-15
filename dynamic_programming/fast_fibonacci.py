"""
Fast Fibonacci — O(log n) using matrix exponentiation / fast doubling.

Uses the identities:
  F(2n)   = F(n) * [2*F(n+1) - F(n)]
  F(2n+1) = F(n+1)^2 + F(n)^2

This allows computing F(n) in O(log n) time, making it feasible to
calculate F(1_000_000) in less than a second.

>>> [fibonacci(i) for i in range(13)]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
>>> fibonacci(0)
0
>>> fibonacci(1)
1
>>> fibonacci(50)
12586269025
>>> fibonacci(-1)
Traceback (most recent call last):
    ...
ValueError: Negative arguments are not supported
"""

from __future__ import annotations


def fibonacci(n: int) -> int:
    """
    Return F(n) using fast doubling in O(log n) time.

    >>> [fibonacci(i) for i in range(13)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
    >>> fibonacci(100)
    354224848179261915075
    """
    if n < 0:
        raise ValueError("Negative arguments are not supported")
    return _fib(n)[0]


def _fib(n: int) -> tuple[int, int]:
    """Return (F(n), F(n+1)) using fast doubling."""
    if n == 0:
        return (0, 1)
    a, b = _fib(n // 2)
    c = a * (b * 2 - a)
    d = a * a + b * b
    return (d, c + d) if n % 2 else (c, d)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    for n in [0, 1, 10, 50, 100]:
        print(f"  fibonacci({n}) = {fibonacci(n)}")
