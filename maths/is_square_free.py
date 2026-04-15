"""
Square-free integer: no prime factor appears with exponent > 1.
Examples of square-free: 1, 2, 3, 5, 6, 7, 10, 11, 13, 14, 15...
NOT square-free: 4 (=2²), 8, 9, 12, 16, 18, 20...

>>> is_square_free([2, 3, 5])
True
>>> is_square_free([2, 2, 3])
False
>>> is_square_free([])
True
>>> is_square_free_integer(30)
True
>>> is_square_free_integer(12)
False
"""


def is_square_free(factors: list[int]) -> bool:
    """Given the prime factor list of n, return True if all factors distinct.

    >>> is_square_free([7, 13])
    True
    """
    return len(factors) == len(set(factors))


def is_square_free_integer(n: int) -> bool:
    """Directly determine whether n is square-free.

    >>> is_square_free_integer(1)
    True
    >>> is_square_free_integer(18)
    False
    """
    if n < 1:
        raise ValueError("n must be positive")
    if n == 1:
        return True
    if n % 4 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % (i * i) == 0:
            return False
        i += 2
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(is_square_free_integer(30), is_square_free_integer(12))
