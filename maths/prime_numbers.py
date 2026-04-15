"""
Prime Numbers
=============
Generate all primes up to n by trial division (slow reference).
"""
import math
from typing import List


def primes_up_to(n: int) -> List[int]:
    """
    >>> primes_up_to(1)
    []
    >>> primes_up_to(10)
    [2, 3, 5, 7]
    >>> primes_up_to(20)
    [2, 3, 5, 7, 11, 13, 17, 19]
    >>> len(primes_up_to(100))
    25
    """
    out: List[int] = []
    for k in range(2, n + 1):
        r = int(math.isqrt(k))
        is_p = True
        for i in range(2, r + 1):
            if k % i == 0:
                is_p = False
                break
        if is_p:
            out.append(k)
    return out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(primes_up_to(50))
    print(f"pi(1000) = {len(primes_up_to(1000))}")
