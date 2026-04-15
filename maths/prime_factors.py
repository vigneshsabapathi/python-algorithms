"""
Prime Factors
=============
Return the multiset (list) of prime factors of a positive integer.
"""
import math
from typing import List


def prime_factors(n: int) -> List[int]:
    """
    >>> prime_factors(12)
    [2, 2, 3]
    >>> prime_factors(1)
    []
    >>> prime_factors(17)
    [17]
    >>> prime_factors(100)
    [2, 2, 5, 5]
    >>> prime_factors(2**10)
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    out: List[int] = []
    while n % 2 == 0:
        out.append(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            out.append(i)
            n //= i
        i += 2
    if n > 1:
        out.append(n)
    return out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (12, 100, 360, 2**7 * 3**3 * 5, 999983):
        print(f"{n} = {prime_factors(n)}")
