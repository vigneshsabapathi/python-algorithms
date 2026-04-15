"""
Lucas numbers: L(0)=2, L(1)=1, L(n)=L(n-1)+L(n-2).
Related to Fibonacci via L(n) = F(n-1) + F(n+1).

>>> lucas(0)
2
>>> lucas(1)
1
>>> lucas(5)
11
>>> [lucas(i) for i in range(8)]
[2, 1, 3, 4, 7, 11, 18, 29]
"""


def lucas(n: int) -> int:
    """Iterative Lucas number.

    >>> lucas(10)
    123
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 2, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def lucas_recursive(n: int) -> int:
    """Naive recursive (exponential)."""
    if n == 0:
        return 2
    if n == 1:
        return 1
    return lucas_recursive(n - 1) + lucas_recursive(n - 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print([lucas(i) for i in range(8)])
