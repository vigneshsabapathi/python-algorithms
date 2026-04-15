"""
Pi Generator (spigot algorithm)
===============================
Generates pi digit-by-digit using the classic Rabinowitz-Wagon spigot.
"""
from typing import Iterator


def pi_digits() -> Iterator[int]:
    """
    Yield decimal digits of pi, one at a time.

    >>> g = pi_digits()
    >>> [next(g) for _ in range(10)]
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    """
    # Jeremy Gibbons streaming algorithm (corrected).
    q, r, t, i = 1, 180, 60, 2
    while True:
        u, y = 3 * (3 * i + 1) * (3 * i + 2), (q * (27 * i - 12) + 5 * r) // (5 * t)
        yield y
        q, r, t, i = 10 * q * i * (2 * i - 1), 10 * u * (q * (5 * i - 2) + r - y * t), t * u, i + 1


def pi_string(n_digits: int) -> str:
    """
    >>> pi_string(1)
    '3'
    >>> pi_string(5)
    '3.1415'
    >>> pi_string(10)
    '3.141592653'
    """
    if n_digits < 1:
        raise ValueError("n_digits must be >= 1")
    g = pi_digits()
    first = str(next(g))
    if n_digits == 1:
        return first
    rest = "".join(str(next(g)) for _ in range(n_digits - 1))
    return f"{first}.{rest}"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(pi_string(50))
