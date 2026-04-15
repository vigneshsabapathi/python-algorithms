"""
Modular division: compute (a / b) mod m, i.e. a * b^(-1) mod m.
Works when gcd(b, m) = 1 (b is invertible mod m).

>>> modular_division(10, 2, 13)
5
>>> modular_division(7, 3, 11)
6
>>> (6 * 3) % 11
7
>>> modular_division(3, 7, 11)
2
"""


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Return (g, x, y) with a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def modular_inverse(a: int, m: int) -> int:
    """a^-1 mod m via extended Euclidean.

    >>> modular_inverse(3, 11)
    4
    """
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    return x % m


def modular_division(a: int, b: int, m: int) -> int:
    """Compute (a / b) mod m.

    >>> modular_division(10, 3, 17)
    9
    """
    return (a % m) * modular_inverse(b, m) % m


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(modular_division(10, 2, 13))
