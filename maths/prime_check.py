"""
Prime Check
===========
Test whether a number is prime.
"""
import math


def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(17)
    True
    >>> is_prime(1)
    False
    >>> is_prime(0)
    False
    >>> is_prime(-7)
    False
    >>> is_prime(100)
    False
    >>> is_prime(97)
    True
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    r = math.isqrt(n)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (2, 3, 4, 17, 25, 97, 100, 7919):
        print(f"{n}: {is_prime(n)}")
