"""
Pollard's Rho (Integer Factorization)
=====================================
Probabilistic factorization algorithm. Expected O(n^(1/4)) per factor found,
far faster than trial division for 20+ digit composites.
"""
import math
import random


def pollard_rho(n: int, seed: int = 2) -> int | None:
    """
    Return a non-trivial factor of composite ``n``, or None if failed.

    >>> pollard_rho(15) in (3, 5)
    True
    >>> pollard_rho(8051) in (83, 97)
    True
    >>> pollard_rho(1009 * 1013) in (1009, 1013)
    True
    """
    if n % 2 == 0:
        return 2
    if n == 1:
        return None

    rng = random.Random(seed)
    while True:
        x = rng.randrange(2, n)
        y = x
        c = rng.randrange(1, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d
        # retry with new seed


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (8051, 10403, 1000003 * 999983):
        f = pollard_rho(n)
        print(f"factor of {n} -> {f} (other: {n // f if f else None})")
