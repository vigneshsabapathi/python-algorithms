"""
Twin Prime
==========
Twin primes are pairs (p, p+2) where both are prime.
"""
import math
from typing import List, Tuple


def is_prime(n: int) -> bool:
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


def twin_primes_up_to(n: int) -> List[Tuple[int, int]]:
    """
    >>> twin_primes_up_to(20)
    [(3, 5), (5, 7), (11, 13), (17, 19)]
    >>> twin_primes_up_to(2)
    []
    >>> len(twin_primes_up_to(100))
    8
    """
    return [(p, p + 2) for p in range(3, n - 1) if is_prime(p) and is_prime(p + 2)]


def twin_of(p: int) -> int:
    """
    Return p+2 if (p, p+2) is a twin-prime pair, else -1.

    >>> twin_of(11)
    13
    >>> twin_of(7)
    -1
    """
    return p + 2 if is_prime(p) and is_prime(p + 2) else -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(twin_primes_up_to(50))
