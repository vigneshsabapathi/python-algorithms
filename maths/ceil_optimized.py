#!/usr/bin/env python3
"""
Optimized ceil variants.

Variants:
1. ceil_math      -- math.ceil; C-level, baseline.
2. ceil_divmod    -- -(-x // 1) trick using integer division semantics.
3. ceil_offset    -- int(x + 0.9999...) for positive floats (fast but lossy).

Run:
    python maths/ceil_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import math

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.ceil import ceil as ceil_ref


def ceil_math(x: float) -> int:
    """
    >>> ceil_math(1.1)
    2
    >>> ceil_math(-1.1)
    -1
    >>> ceil_math(0)
    0
    """
    return math.ceil(x)


def ceil_divmod(x: float) -> int:
    """
    Uses -(-x // 1) which is exact for floats w/o the `int()` truncation.

    >>> ceil_divmod(1.1)
    2
    >>> ceil_divmod(-1.1)
    -1
    >>> ceil_divmod(5)
    5
    """
    return int(-(-x // 1))


def _benchmark() -> None:
    vals = [i * 0.37 - 50 for i in range(300)]
    n = 20000
    t1 = timeit.timeit(lambda: [ceil_ref(v) for v in vals], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [ceil_math(v) for v in vals], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [ceil_divmod(v) for v in vals], number=n) * 1000 / n
    print(f"reference:   {t1:.4f} ms")
    print(f"math.ceil:   {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"divmod:      {t3:.4f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
