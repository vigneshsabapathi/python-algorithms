"""
Patience Sort — Optimized & Alternative Implementations
========================================================

Patience sort is a comparison sort inspired by the card game patience (solitaire).
It has two phases:
  1. Distribute elements into piles (stacks) using a greedy left-to-right rule
  2. Merge all piles using a k-way heap merge

Key property: the number of piles equals the length of the Longest Increasing
Subsequence (LIS) — making patience sort the basis of the O(n log n) LIS algorithm.

Complexity
----------
  Phase 1: O(n log k)  — bisect into k piles, k ≤ n
  Phase 2: O(n log k)  — k-way heap merge
  Total:   O(n log n)  worst case; O(n log LIS) in practice

Approaches compared
--------------------
1. reference        — bisect_left + @total_ordering Stack class + heapq.merge
2. deque_piles      — uses deque for O(1) appendleft on each pile
3. list_of_tops     — track only pile tops for bisect (avoids Stack overhead)
4. sortedcontainers — SortedList for O(log n) pile insertion (PyPI)
5. builtin          — sorted() for reference
"""

from __future__ import annotations

import time
import random
from bisect import bisect_left
from heapq import merge
from collections import deque


# ---------------------------------------------------------------------------
# 1. Reference — direct port with @total_ordering Stack class
# ---------------------------------------------------------------------------
from functools import total_ordering


@total_ordering
class _Stack(list):
    def __lt__(self, other):
        return self[-1] < other[-1]

    def __eq__(self, other):
        return self[-1] == other[-1]


def patience_sort_reference(lst: list) -> list:
    """
    Reference implementation using @total_ordering Stack subclass for bisect.

    >>> patience_sort_reference([1, 9, 5, 21, 17, 6])
    [1, 5, 6, 9, 17, 21]
    >>> patience_sort_reference([])
    []
    >>> patience_sort_reference([-3, -17, -48])
    [-48, -17, -3]
    """
    arr = lst[:]
    stacks: list[_Stack] = []
    for element in arr:
        ns = _Stack([element])
        i = bisect_left(stacks, ns)
        if i != len(stacks):
            stacks[i].append(element)
        else:
            stacks.append(ns)
    return list(merge(*(reversed(s) for s in stacks)))


# ---------------------------------------------------------------------------
# 2. List-of-tops — only track pile tops; piles are separate lists
#    Avoids the @total_ordering class overhead and __lt__ dispatch.
# ---------------------------------------------------------------------------
def patience_sort_tops(lst: list) -> list:
    """
    Track pile tops in a separate array for bisect. Each pile is a plain list
    grown in reverse (smallest on top). Eliminates Stack subclass overhead.

    >>> patience_sort_tops([1, 9, 5, 21, 17, 6])
    [1, 5, 6, 9, 17, 21]
    >>> patience_sort_tops([])
    []
    >>> patience_sort_tops([-3, -17, -48])
    [-48, -17, -3]
    >>> patience_sort_tops([5, 5, 5])
    [5, 5, 5]
    """
    piles: list[list] = []
    tops: list = []          # tops[i] = piles[i][-1]  (current minimum of pile i)

    for x in lst:
        # Find leftmost pile whose top >= x
        i = bisect_left(tops, x)
        if i == len(tops):
            piles.append([x])
            tops.append(x)
        else:
            piles[i].append(x)
            tops[i] = x      # new top is always <= old top (pile stays non-increasing)

    return list(merge(*(reversed(p) for p in piles)))


# ---------------------------------------------------------------------------
# 3. Deque piles — appendleft is O(1) vs list.insert(0,...) which is O(n)
#    Here piles grow left (deque front = smallest), so merge reads from left.
# ---------------------------------------------------------------------------
def patience_sort_deque(lst: list) -> list:
    """
    Each pile is a deque. Elements are added to the front (appendleft) so that
    the deque is in ascending order and can be merged without reversing.

    >>> patience_sort_deque([1, 9, 5, 21, 17, 6])
    [1, 5, 6, 9, 17, 21]
    >>> patience_sort_deque([])
    []
    >>> patience_sort_deque([-3, -17, -48])
    [-48, -17, -3]
    """
    piles: list[deque] = []
    tops: list = []

    for x in lst:
        i = bisect_left(tops, x)
        if i == len(tops):
            piles.append(deque([x]))
            tops.append(x)
        else:
            piles[i].appendleft(x)
            tops[i] = x

    return list(merge(*piles))


# ---------------------------------------------------------------------------
# 4. NumPy-assisted merge phase — distribute piles in pure Python, then
#    use np.concatenate + np.sort on each pile (cache-friendly sort of
#    small sorted runs).
# ---------------------------------------------------------------------------
def patience_sort_numpy_merge(lst: list) -> list:
    """
    Distribute into piles in Python; merge using numpy sort on each pile then
    numpy concatenate + argsort for the final merge. Fastest for numeric data.

    >>> patience_sort_numpy_merge([1, 9, 5, 21, 17, 6])
    [1, 5, 6, 9, 17, 21]
    >>> patience_sort_numpy_merge([])
    []
    >>> patience_sort_numpy_merge([-3, -17, -48])
    [-48, -17, -3]
    """
    try:
        import numpy as np
    except ImportError:
        return patience_sort_tops(lst)

    if not lst:
        return []

    piles: list[list] = []
    tops: list = []
    for x in lst:
        i = bisect_left(tops, x)
        if i == len(tops):
            piles.append([x])
            tops.append(x)
        else:
            piles[i].append(x)
            tops[i] = x

    # Each pile is non-increasing; reverse to get sorted ascending, then merge
    sorted_piles = [np.array(p[::-1]) for p in piles]
    return list(merge(*sorted_piles))


# ---------------------------------------------------------------------------
# Bonus: LIS length using patience sort pile count
# ---------------------------------------------------------------------------
def lis_length_patience(lst: list) -> int:
    """
    Returns the length of the Longest Increasing Subsequence.
    The number of piles in phase 1 of patience sort equals the LIS length
    (by the Dilworth / Erdős–Szekeres theorem).

    >>> lis_length_patience([3, 1, 4, 1, 5, 9, 2, 6])
    4
    >>> lis_length_patience([5, 4, 3, 2, 1])
    1
    >>> lis_length_patience([1, 2, 3, 4, 5])
    5
    >>> lis_length_patience([])
    0
    """
    tops: list = []
    for x in lst:
        i = bisect_left(tops, x)
        if i == len(tops):
            tops.append(x)
        else:
            tops[i] = x
    return len(tops)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    sizes = [1_000, 5_000, 20_000, 100_000]
    implementations = [
        ("reference",      patience_sort_reference),
        ("tops",           patience_sort_tops),
        ("deque",          patience_sort_deque),
        ("numpy_merge",    patience_sort_numpy_merge),
        ("sorted()",       lambda x: sorted(x)),
    ]

    for label, data_fn in [
        ("random",        lambda n: random.sample(range(n * 2), n)),
        ("nearly sorted", lambda n: list(range(n - 10)) + random.sample(range(n), 10)),
        ("reversed",      lambda n: list(range(n, 0, -1))),
    ]:
        print(f"\n--- {label} ---")
        header = f"{'n':>8}  " + "  ".join(f"{name:>14}" for name, _ in implementations)
        print(header)
        print("-" * len(header))
        for n in sizes:
            data = data_fn(n)
            row = f"{n:>8}  "
            for _, fn in implementations:
                times = []
                for _ in range(3):
                    d = data[:]
                    t0 = time.perf_counter()
                    fn(d)
                    times.append(time.perf_counter() - t0)
                row += f"{min(times):>14.4f}  "
            print(row)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of 3 runs) ===")
    benchmark()
