#!/usr/bin/env python3
"""
Optimized mode variants.

Reference: O(n^2) — uses input_list.count inside a list comp.

Variants:
1. mode_counter    -- collections.Counter, O(n) single pass.
2. mode_multimode  -- statistics.multimode() (Python 3.8+), C-level.
3. mode_manual_dict -- manual dict accumulator, teaching variant.

Run:
    python maths/average_mode_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import random
import statistics
from collections import Counter
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.average_mode import mode as mode_reference


def mode_counter(input_list: list) -> list[Any]:
    """
    O(n) via Counter — single pass, then pick most_common count.

    >>> mode_counter([2, 3, 4, 5, 3, 4, 2, 5, 2, 2, 4, 2, 2, 2])
    [2]
    >>> mode_counter([3, 4, 5, 3, 4, 2, 5, 2, 2, 4, 4, 4, 2, 2, 4, 2])
    [2, 4]
    """
    if not input_list:
        return []
    c = Counter(input_list)
    top = max(c.values())
    return sorted([k for k, v in c.items() if v == top])


def mode_multimode(input_list: list) -> list[Any]:
    """
    >>> sorted(mode_multimode([2, 3, 4, 5, 3, 4, 2, 5, 2, 2, 4, 2, 2, 2]))
    [2]
    """
    return sorted(statistics.multimode(input_list)) if input_list else []


def _benchmark() -> None:
    random.seed(0)
    data = [random.randint(0, 50) for _ in range(5000)]
    n = 100
    t1 = timeit.timeit(lambda: mode_reference(data), number=n) * 1000 / n
    t2 = timeit.timeit(lambda: mode_counter(data), number=n) * 1000 / n
    t3 = timeit.timeit(lambda: mode_multimode(data), number=n) * 1000 / n
    print(f"reference O(n^2): {t1:.3f} ms")
    print(f"counter O(n):     {t2:.3f} ms  [{t1/t2:.0f}x faster]")
    print(f"multimode O(n):   {t3:.3f} ms  [{t1/t3:.0f}x faster]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
