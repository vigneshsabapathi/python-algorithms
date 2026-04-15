"""
Sieve of Eratosthenes
=====================
Classical sieve (same as prime_sieve_eratosthenes; kept separately to mirror
TheAlgorithms repo layout).
"""
import math
from typing import List


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    Return list of primes <= n.

    >>> sieve_of_eratosthenes(20)
    [2, 3, 5, 7, 11, 13, 17, 19]
    >>> sieve_of_eratosthenes(0)
    []
    >>> sieve_of_eratosthenes(2)
    [2]
    """
    if n < 2:
        return []
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i in range(n + 1) if is_prime[i]]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(sieve_of_eratosthenes(50))
