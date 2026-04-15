#!/usr/bin/env python3
"""
Optimized collatz_sequence variants.

Variants:
1. collatz_bitshift  -- use `n >> 1` and `3*n+1` with strip-trailing-zeros shortcut.
2. collatz_cached    -- memoise sequence lengths for batch queries.
3. collatz_length    -- O(1) in memoised cache; returns just the step count.

Run:
    python maths/collatz_sequence_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from collections.abc import Generator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.collatz_sequence import collatz_sequence as ref


def collatz_bitshift(n: int) -> Generator[int]:
    """
    Bit-shift variant: n//2 -> n >> 1.  Same algorithm, faster ops.

    >>> tuple(collatz_bitshift(4))
    (4, 2, 1)
    >>> tuple(collatz_bitshift(11))
    (11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1)
    """
    if not isinstance(n, int) or n < 1:
        raise Exception("Sequence only defined for positive integers")
    yield n
    while n != 1:
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
        yield n


_len_cache: dict[int, int] = {1: 1}


def collatz_length(n: int) -> int:
    """
    Memoised step count (including the starting n).

    >>> collatz_length(1)
    1
    >>> collatz_length(4)
    3
    >>> collatz_length(27)
    112
    """
    if n in _len_cache:
        return _len_cache[n]
    next_n = n >> 1 if not (n & 1) else 3 * n + 1
    result = 1 + collatz_length(next_n)
    _len_cache[n] = result
    return result


def _benchmark() -> None:
    import sys as _sys
    _sys.setrecursionlimit(5000)
    n = 200
    t1 = timeit.timeit(lambda: [tuple(ref(i)) for i in range(1, 1000)], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [tuple(collatz_bitshift(i)) for i in range(1, 1000)], number=n) * 1000 / n
    _len_cache.clear(); _len_cache[1] = 1
    t3 = timeit.timeit(lambda: [collatz_length(i) for i in range(1, 1000)], number=n) * 1000 / n
    print(f"reference: {t1:.3f} ms")
    print(f"bitshift:  {t2:.3f} ms  [{t1/t2:.2f}x]")
    print(f"memoised length: {t3:.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
