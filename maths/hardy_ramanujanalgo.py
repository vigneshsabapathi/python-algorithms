"""
Hardy-Ramanujan theorem: almost all integers n have approximately
log(log(n)) distinct prime factors.

This module provides omega(n) — the count of distinct prime factors of n.

>>> exact_prime_factor_count(12)
2
>>> exact_prime_factor_count(30)
3
>>> exact_prime_factor_count(1)
0
>>> exact_prime_factor_count(100)
2
"""

import math


def exact_prime_factor_count(n: int) -> int:
    """Count distinct prime factors of n (omega(n)).

    >>> exact_prime_factor_count(2520)
    4
    """
    count = 0
    if n % 2 == 0:
        count += 1
        while n % 2 == 0:
            n //= 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            count += 1
            while n % i == 0:
                n //= i
        i += 2
    if n > 1:
        count += 1
    return count


def hardy_ramanujan_estimate(n: int) -> float:
    """Asymptotic estimate ≈ log(log(n))."""
    if n < 3:
        return 0.0
    return math.log(math.log(n))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(exact_prime_factor_count(30), hardy_ramanujan_estimate(30))
