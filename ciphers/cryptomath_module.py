"""
Cryptomath Module — modular arithmetic utilities for classical cipher implementations.

Provides modular inverse calculation used by the Affine cipher and others.

References:
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
"""

from math import gcd


def find_mod_inverse(a: int, m: int) -> int:
    """
    Find the modular multiplicative inverse of a modulo m using the
    extended Euclidean algorithm.

    Returns x such that (a * x) % m == 1.

    Raises ValueError if gcd(a, m) != 1 (inverse does not exist).

    >>> find_mod_inverse(7, 26)
    15
    >>> find_mod_inverse(3, 94)
    63
    >>> find_mod_inverse(11, 26)
    19
    >>> find_mod_inverse(4, 26)
    Traceback (most recent call last):
        ...
    ValueError: mod inverse of 4 and 26 does not exist
    """
    if gcd(a, m) != 1:
        raise ValueError(f"mod inverse of {a!r} and {m!r} does not exist")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            (u1 - q * v1),
            (u2 - q * v2),
            (u3 - q * v3),
            v1,
            v2,
            v3,
        )
    return u1 % m


if __name__ == "__main__":
    import doctest
    doctest.testmod()
