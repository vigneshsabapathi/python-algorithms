"""
Fibonacci sequence: F(0)=0, F(1)=1, F(n)=F(n-1)+F(n-2).

>>> fib_iter(10)
55
>>> fib_iter(0)
0
>>> fib_iter(1)
1
>>> [fib_iter(i) for i in range(8)]
[0, 1, 1, 2, 3, 5, 8, 13]
"""


def fib_iter(n: int) -> int:
    """Iterative O(n).

    >>> fib_iter(20)
    6765
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fib_recursive(n: int) -> int:
    """Naive recursive O(2^n) — for small n only."""
    if n < 2:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print([fib_iter(i) for i in range(10)])
