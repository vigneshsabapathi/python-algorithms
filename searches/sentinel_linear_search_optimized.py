#!/usr/bin/env python3

"""
Optimized and alternative implementations of sentinel linear search.

Variants covered:
1. sentinel_immutable       — sentinel trick on a copy (no mutation of input)
2. linear_enumerate         — plain enumerate loop (baseline, no sentinel)
3. list_index               — list.index() C-backed linear scan (fastest linear)
4. bisect_search            — bisect.bisect_left for SORTED sequences (O(log n))

The sentinel trick eliminates the per-iteration bounds check (index < n), saving
one comparison per iteration vs a standard while loop. In Python the gain is modest
because the interpreter overhead dwarfs the check, but the concept is important
for C-level implementations and interview discussions.

Run benchmarks:
    python searches/sentinel_linear_search_optimized.py
"""

from __future__ import annotations

import bisect


# ---------------------------------------------------------------------------
# Variant 1 — sentinel on a copy (no side-effects on caller's list)
# ---------------------------------------------------------------------------


def sentinel_immutable(sequence: list, target) -> int | None:
    """
    Sentinel linear search that never mutates the caller's list.

    Creates a shallow copy, appends the sentinel, searches, then discards
    the copy. Same O(n) algorithm; O(n) extra space for the copy.

    Returns index (int) on hit, None on miss — consistent with original.

    >>> sentinel_immutable([0, 5, 7, 10, 15], 0)
    0
    >>> sentinel_immutable([0, 5, 7, 10, 15], 15)
    4
    >>> sentinel_immutable([0, 5, 7, 10, 15], 5)
    1
    >>> sentinel_immutable([0, 5, 7, 10, 15], 6) is None
    True
    >>> sentinel_immutable([], 5) is None
    True
    >>> sentinel_immutable([42], 42)
    0
    """
    seq = list(sequence)   # copy — caller's list unchanged
    seq.append(target)
    index = 0
    while seq[index] != target:
        index += 1
    if index == len(sequence):   # past original end -> miss
        return None
    return index


# ---------------------------------------------------------------------------
# Variant 2 — plain enumerate loop (cleaner, same complexity)
# ---------------------------------------------------------------------------


def linear_enumerate(sequence: list, target) -> int | None:
    """
    Standard enumerate loop — no sentinel, cleaner code, same O(n).

    >>> linear_enumerate([0, 5, 7, 10, 15], 0)
    0
    >>> linear_enumerate([0, 5, 7, 10, 15], 15)
    4
    >>> linear_enumerate([0, 5, 7, 10, 15], 5)
    1
    >>> linear_enumerate([0, 5, 7, 10, 15], 6) is None
    True
    >>> linear_enumerate([], 5) is None
    True
    """
    for i, v in enumerate(sequence):
        if v == target:
            return i
    return None


# ---------------------------------------------------------------------------
# Variant 3 — list.index() C-backed (fastest linear for lists)
# ---------------------------------------------------------------------------


def list_index_search(sequence: list, target) -> int | None:
    """
    list.index() — C-backed linear scan; try/except to match None interface.

    >>> list_index_search([0, 5, 7, 10, 15], 0)
    0
    >>> list_index_search([0, 5, 7, 10, 15], 15)
    4
    >>> list_index_search([0, 5, 7, 10, 15], 5)
    1
    >>> list_index_search([0, 5, 7, 10, 15], 6) is None
    True
    >>> list_index_search([], 5) is None
    True
    """
    try:
        return sequence.index(target)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Variant 4 — bisect (SORTED sequences only, O(log n))
# ---------------------------------------------------------------------------


def bisect_search(sequence: list, target) -> int | None:
    """
    bisect.bisect_left — O(log n) for SORTED sequences only.

    Included as a performance baseline showing the gain from sorting.

    >>> bisect_search([0, 5, 7, 10, 15], 0)
    0
    >>> bisect_search([0, 5, 7, 10, 15], 15)
    4
    >>> bisect_search([0, 5, 7, 10, 15], 5)
    1
    >>> bisect_search([0, 5, 7, 10, 15], 6) is None
    True
    >>> bisect_search([], 5) is None
    True
    """
    if not sequence:
        return None
    idx = bisect.bisect_left(sequence, target)
    if idx < len(sequence) and sequence[idx] == target:
        return idx
    return None


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import random
    import timeit
    import sys
    import os

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.sentinel_linear_search import sentinel_linear_search

    REPS = 500

    for size in [100, 1_000, 10_000]:
        random.seed(42)
        data_u = list(range(size))   # unsorted-ish but predictable
        random.shuffle(data_u)
        data_s = sorted(data_u)

        targets_hit  = random.choices(data_u, k=REPS)
        targets_miss = [size + random.randint(1, size) for _ in range(REPS)]
        targets = targets_hit + targets_miss

        print(f"\n{'='*62}")
        print(f"  n = {size:,}  ({REPS*2} lookups: {REPS} hits + {REPS} misses)")
        print(f"{'='*62}")

        fns = [
            ("sentinel original (mutates)",    lambda t: sentinel_linear_search(data_u[:], t)),
            ("sentinel_immutable (copy)",       lambda t: sentinel_immutable(data_u, t)),
            ("linear_enumerate (no sentinel)",  lambda t: linear_enumerate(data_u, t)),
            ("list.index (C-backed)",           lambda t: list_index_search(data_u, t)),
            ("bisect (sorted, O(log n))",       lambda t: bisect_search(data_s, t)),
        ]

        results = {}
        for name, fn in fns:
            t = timeit.timeit(lambda fn=fn: [fn(x) for x in targets], number=5)
            results[name] = t
            print(f"  {name:<44}  {t*1000/5:8.3f} ms/run")

        best = min(results, key=results.get)
        print(f"\n  Winner: {best}")

    print("\n=== Sentinel advantage analysis ===")
    print("  Standard while loop checks: (index < n) AND (arr[index] != target)")
    print("  Sentinel while loop checks: (arr[index] != target) only")
    print("  Saving: 1 comparison per iteration")
    print("  In C: ~25% speedup at tight loop level")
    print("  In Python: negligible (interpreter overhead dominates)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
