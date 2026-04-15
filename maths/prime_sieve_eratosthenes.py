"""
Prime Sieve (Eratosthenes)
==========================
Return all primes up to ``n`` inclusive.
"""
import math
from typing import List


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    >>> sieve_of_eratosthenes(10)
    [2, 3, 5, 7]
    >>> sieve_of_eratosthenes(1)
    []
    >>> sieve_of_eratosthenes(2)
    [2]
    >>> sieve_of_eratosthenes(30)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if n < 2:
        return []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return [i for i, v in enumerate(is_prime) if v]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(sieve_of_eratosthenes(50))
    print(f"pi(1_000_000) = {len(sieve_of_eratosthenes(1_000_000))}")
