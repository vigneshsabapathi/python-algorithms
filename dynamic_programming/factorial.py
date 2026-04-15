"""
Factorial using memoization (Dynamic Programming).

The factorial of n (n!) is the product of all positive integers <= n.
Uses Python's built-in lru_cache for automatic memoization.

>>> factorial(7)
5040
>>> factorial(0)
1
>>> factorial(1)
1
>>> factorial(10)
3628800
>>> factorial(-1)
Traceback (most recent call last):
    ...
ValueError: Number should not be negative.
>>> [factorial(i) for i in range(10)]
[1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
"""

from functools import lru_cache


@lru_cache
def factorial(num: int) -> int:
    """
    Calculate factorial of num using memoization.

    >>> factorial(7)
    5040
    >>> factorial(-1)
    Traceback (most recent call last):
      ...
    ValueError: Number should not be negative.
    >>> [factorial(i) for i in range(10)]
    [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
    """
    if num < 0:
        raise ValueError("Number should not be negative.")
    return 1 if num in (0, 1) else num * factorial(num - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    for n in [0, 1, 5, 10, 15, 20]:
        print(f"  factorial({n}) = {factorial(n)}")
