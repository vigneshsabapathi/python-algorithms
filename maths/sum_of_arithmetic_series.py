"""
Sum of Arithmetic Series
========================
Closed-form sum S_n = n/2 · (2a + (n-1)d) where a is first term, d common diff.
"""


def arithmetic_sum(first: float, common: float, n: int) -> float:
    """
    >>> arithmetic_sum(1, 1, 10)   # 1+2+...+10
    55.0
    >>> arithmetic_sum(2, 3, 5)    # 2,5,8,11,14 -> 40
    40.0
    >>> arithmetic_sum(1, 0, 5)    # constant 1 five times
    5.0
    >>> arithmetic_sum(5, 1, 0)
    0.0
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return n / 2 * (2 * first + (n - 1) * common)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(arithmetic_sum(1, 1, 100))
    print(arithmetic_sum(2, 3, 10))
