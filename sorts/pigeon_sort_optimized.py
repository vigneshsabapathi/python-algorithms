"""
Pigeon Hole Sort — Optimized & Alternative Implementations
===========================================================

Pigeon hole sort (also called pigeonhole sort) is a non-comparison integer sort.
It allocates one "hole" per distinct value in [min, max], counts occurrences,
then reads the holes back in order.

It is essentially counting sort with a different framing:
  - Counting sort: counts[v - min] = # occurrences → write back in O(n + range)
  - Pigeon sort:   holes[v - min]  = v itself (redundant), holes_repeat = count

Both are O(n + k) time and O(k) space where k = max - min + 1.

Approaches compared
--------------------
1. reference      — original: two arrays (holes + holes_repeat), O(n + k) space
2. counting       — one array (counts only), reconstruct values from index + min
3. dict_sparse    — dict-based: O(n) space, handles large ranges with few distinct values
4. numpy_bin      — np.bincount for vectorised counting (fastest for numeric data)
5. builtin        — sorted() for reference
"""

from __future__ import annotations

import time
import random
from collections import defaultdict


# ---------------------------------------------------------------------------
# 1. Reference — direct port (two arrays: holes + holes_repeat)
# ---------------------------------------------------------------------------
def pigeon_sort_reference(lst: list[int]) -> list[int]:
    """
    Original two-array implementation.

    >>> pigeon_sort_reference([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pigeon_sort_reference([])
    []
    >>> pigeon_sort_reference([-2, -5, -45])
    [-45, -5, -2]
    """
    if not lst:
        return []
    arr = lst[:]
    _min, _max = min(arr), max(arr)
    holes_range = _max - _min + 1
    holes = [0] * holes_range
    holes_repeat = [0] * holes_range
    for v in arr:
        idx = v - _min
        holes[idx] = v
        holes_repeat[idx] += 1
    out = []
    for i in range(holes_range):
        out.extend([holes[i]] * holes_repeat[i])
    return out


# ---------------------------------------------------------------------------
# 2. Counting sort — one array only; reconstruct value as i + _min
#    Eliminates the redundant holes[] array (saves O(k) space)
# ---------------------------------------------------------------------------
def pigeon_sort_counting(lst: list[int]) -> list[int]:
    """
    Streamlined counting sort: only track counts, reconstruct values on output.
    Saves half the O(k) space compared to reference.

    >>> pigeon_sort_counting([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pigeon_sort_counting([])
    []
    >>> pigeon_sort_counting([-2, -5, -45])
    [-45, -5, -2]
    >>> pigeon_sort_counting([5, 5, 5])
    [5, 5, 5]
    """
    if not lst:
        return []
    _min, _max = min(lst), max(lst)
    counts = [0] * (_max - _min + 1)
    for v in lst:
        counts[v - _min] += 1
    return [i + _min for i, c in enumerate(counts) for _ in range(c)]


# ---------------------------------------------------------------------------
# 3. Dict-based (sparse) — O(n) space regardless of value range
#    Best when range >> n (e.g., sort [1, 1_000_000] without allocating 1M slots)
# ---------------------------------------------------------------------------
def pigeon_sort_sparse(lst: list[int]) -> list[int]:
    """
    Uses a dict to count occurrences. O(n) space, O(n log n) time due to
    sorted() on keys. Ideal when value range is large but few distinct values.

    >>> pigeon_sort_sparse([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pigeon_sort_sparse([])
    []
    >>> pigeon_sort_sparse([-2, -5, -45])
    [-45, -5, -2]
    >>> pigeon_sort_sparse([1000000, -1000000, 0])
    [-1000000, 0, 1000000]
    """
    if not lst:
        return []
    counts: dict[int, int] = defaultdict(int)
    for v in lst:
        counts[v] += 1
    return [v for v in sorted(counts) for _ in range(counts[v])]


# ---------------------------------------------------------------------------
# 4. NumPy bincount — vectorised counting; fastest for non-negative or
#    shifted-to-non-negative integer arrays
# ---------------------------------------------------------------------------
def pigeon_sort_numpy(lst: list[int]) -> list[int]:
    """
    Uses np.bincount for O(n + k) counting in C. Fastest for numeric data.

    >>> pigeon_sort_numpy([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> pigeon_sort_numpy([])
    []
    >>> pigeon_sort_numpy([-2, -5, -45])
    [-45, -5, -2]
    """
    if not lst:
        return []
    try:
        import numpy as np
    except ImportError:
        return pigeon_sort_counting(lst)
    arr = np.array(lst)
    _min = int(arr.min())
    counts = np.bincount(arr - _min)
    return np.repeat(np.arange(len(counts)) + _min, counts).tolist()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    implementations = [
        ("reference",  pigeon_sort_reference),
        ("counting",   pigeon_sort_counting),
        ("sparse",     pigeon_sort_sparse),
        ("numpy",      pigeon_sort_numpy),
        ("sorted()",   lambda x: sorted(x)),
    ]

    print("\n--- small range (values in [0, 1000]), varying n ---")
    sizes = [1_000, 10_000, 100_000, 500_000]
    header = f"{'n':>8}  " + "  ".join(f"{name:>12}" for name, _ in implementations)
    print(header)
    print("-" * len(header))
    for n in sizes:
        data = [random.randint(0, 1000) for _ in range(n)]
        row = f"{n:>8}  "
        for _, fn in implementations:
            times = [
                (lambda d=data[:]: (
                    __import__('time').perf_counter(),
                    fn(d),
                    __import__('time').perf_counter()
                ))()
                for _ in range(3)
            ]
            # simpler approach
            best = float("inf")
            for _ in range(3):
                d = data[:]
                t0 = time.perf_counter()
                fn(d)
                best = min(best, time.perf_counter() - t0)
            row += f"{best:>12.4f}  "
        print(row)

    print("\n--- large range (values in [-500000, 500000]), n=1000 ---")
    print("(pigeon/counting allocate 1M slots; dict_sparse allocates only n)")
    data = random.sample(range(-500_000, 500_001), 1000)
    row2 = f"{'n=1000':>8}  "
    for _, fn in implementations:
        best = float("inf")
        for _ in range(3):
            d = data[:]
            t0 = time.perf_counter()
            fn(d)
            best = min(best, time.perf_counter() - t0)
        row2 += f"{best:>12.4f}  "
    print(f"{'n':>8}  " + "  ".join(f"{name:>12}" for name, _ in implementations))
    print("-" * len(header))
    print(row2)

    print("\n--- n=10000, varying value range ---")
    header3 = f"{'range':>12}  " + "  ".join(f"{name:>12}" for name, _ in implementations)
    print(header3)
    print("-" * len(header3))
    for r in [100, 1_000, 10_000, 100_000, 1_000_000]:
        data = [random.randint(0, r) for _ in range(10_000)]
        row3 = f"{r:>12}  "
        for _, fn in implementations:
            best = float("inf")
            for _ in range(3):
                d = data[:]
                t0 = time.perf_counter()
                fn(d)
                best = min(best, time.perf_counter() - t0)
            row3 += f"{best:>12.4f}  "
        print(row3)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of 3 runs) ===")
    benchmark()
