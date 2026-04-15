"""
Segmented Sieve
===============
Produce primes in [lo, hi] without allocating a full 0..hi sieve, useful when
hi is huge but the range is small.
"""
import math
from typing import List


def segmented_sieve(lo: int, hi: int) -> List[int]:
    """
    >>> segmented_sieve(10, 30)
    [11, 13, 17, 19, 23, 29]
    >>> segmented_sieve(1, 10)
    [2, 3, 5, 7]
    >>> segmented_sieve(100, 120)
    [101, 103, 107, 109, 113]
    """
    if hi < 2:
        return []
    lo = max(lo, 2)
    r = int(math.isqrt(hi))

    # sieve primes up to sqrt(hi)
    small = [True] * (r + 1)
    small[0] = small[1] = False
    for i in range(2, int(math.isqrt(r)) + 1):
        if small[i]:
            for j in range(i * i, r + 1, i):
                small[j] = False
    base_primes = [i for i, v in enumerate(small) if v]

    # sieve [lo, hi]
    size = hi - lo + 1
    mark = bytearray([1]) * size
    for p in base_primes:
        start = max(p * p, ((lo + p - 1) // p) * p)
        for j in range(start, hi + 1, p):
            mark[j - lo] = 0
    return [lo + i for i in range(size) if mark[i] and (lo + i) >= 2]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(segmented_sieve(10**6, 10**6 + 100))
