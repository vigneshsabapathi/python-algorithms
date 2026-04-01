"""
Bogo sort variants for interview context.

Bogosort is intentionally terrible — it exists to illustrate why algorithm
analysis matters. This file benchmarks three variants and compares them with
sorted() to make the absurdity concrete.

Variants:
1. bozo_sort       — swap exactly two random elements per step instead of a
                     full shuffle.  Same expected O(n × n!) time but cheaper
                     per iteration; converges faster for nearly-sorted inputs.
2. permutation_sort — deterministic bogo: try every permutation in lexicographic
                     order until sorted.  Guaranteed to terminate in ≤ n!
                     attempts; no randomness, but still O(n × n!) worst case.
3. sorted()         — Timsort O(n log n), shown for scale.

Expected shuffles/swaps:
  bogo_sort:   E[shuffles] = n!       (geometric(1/n!))
  bozo_sort:   E[swaps]   ≈ n × n!   (each swap fixes 1/n of the disorder)
  perm_sort:   worst      = n!        (deterministic, no variance)

Key interview insight: bogo sort is the canonical example of an algorithm
with unbounded expected time. For n = 20, E[shuffles] = 20! ≈ 2.4 × 10^18.
At 10^9 shuffles/sec that's ~77 billion years.
"""

from __future__ import annotations

import itertools
import random


# ──────────────────────────────────────────────────────────────────────────────
# Pythonic is_sorted helper
# ──────────────────────────────────────────────────────────────────────────────

def _is_sorted(seq: list) -> bool:
    """O(n) sorted check using zip — more idiomatic than an index loop."""
    return all(a <= b for a, b in zip(seq, seq[1:]))


# ──────────────────────────────────────────────────────────────────────────────
# 1. Bozo sort — swap two random elements per step
# ──────────────────────────────────────────────────────────────────────────────

def bozo_sort(collection: list) -> list:
    """
    Randomly swap two elements until the list is sorted.
    Each step is cheaper than a full shuffle (O(1) vs O(n)) but expected
    total swaps is O(n × n!) — same asymptotic class.

    >>> bozo_sort([3, 1, 2])
    [1, 2, 3]
    >>> bozo_sort([])
    []
    >>> bozo_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> bozo_sort([1])
    [1]
    """
    arr = list(collection)
    n = len(arr)
    while not _is_sorted(arr):
        i, j = random.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


# ──────────────────────────────────────────────────────────────────────────────
# 2. Deterministic permutation sort
# ──────────────────────────────────────────────────────────────────────────────

def permutation_sort(collection: list) -> list:
    """
    Try every permutation in lexicographic order until one is sorted.
    Deterministic — guaranteed to terminate in ≤ n! attempts.
    Still O(n × n!) worst case, but no randomness and no infinite loops.

    >>> permutation_sort([3, 1, 2])
    [1, 2, 3]
    >>> permutation_sort([])
    []
    >>> permutation_sort([-2, -5, -45])
    [-45, -5, -2]
    >>> permutation_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    """
    for perm in itertools.permutations(collection):
        if _is_sorted(list(perm)):
            return list(perm)
    return list(collection)


# ──────────────────────────────────────────────────────────────────────────────
# Benchmark
# ──────────────────────────────────────────────────────────────────────────────

def benchmark() -> None:
    import math
    import timeit

    from sorts.bogo_sort import bogo_sort

    random.seed(42)

    print("Expected shuffles vs actual (100 trials each):")
    print(f"  {'n':<4} {'E[n!]':>8} {'bogo avg':>10} {'bozo avg':>10}")
    print("  " + "-" * 36)
    for n in [3, 4, 5, 6]:
        bogo_counts, bozo_counts = [], []
        for _ in range(100):
            arr = list(range(n))
            random.shuffle(arr)

            # bogo
            a = list(arr)
            c = 0
            while not _is_sorted(a):
                random.shuffle(a)
                c += 1
            bogo_counts.append(c)

            # bozo
            a = list(arr)
            c = 0
            while not _is_sorted(a):
                i, j = random.sample(range(n), 2)
                a[i], a[j] = a[j], a[i]
                c += 1
            bozo_counts.append(c)

        print(f"  n={n}  {math.factorial(n):>8}  "
              f"{sum(bogo_counts)/100:>10.1f}  {sum(bozo_counts)/100:>10.1f}")

    print()
    print("Timing on n=6 (500 trials each):")
    data6 = [6, 5, 4, 3, 2, 1]
    t_bogo = timeit.timeit(lambda: bogo_sort(list(data6)), number=500)
    t_bozo = timeit.timeit(lambda: bozo_sort(list(data6)), number=500)
    t_perm = timeit.timeit(lambda: permutation_sort(list(data6)), number=500)
    t_sort = timeit.timeit(lambda: sorted(data6), number=500)
    print(f"  bogo_sort:        {t_bogo:.3f}s")
    print(f"  bozo_sort:        {t_bozo:.3f}s")
    print(f"  permutation_sort: {t_perm:.3f}s")
    print(f"  sorted():         {t_sort:.4f}s")

    print()
    print("Scale comparison - sorted() on n=1000 vs bogo_sort theory:")
    t_sorted_1000 = timeit.timeit(
        lambda: sorted(random.sample(range(1000), 1000)), number=1000
    )
    print(f"  sorted() on n=1000 (1000 iters):  {t_sorted_1000:.3f}s")
    print(f"  bogo_sort n=10 expected shuffles: {math.factorial(10):,}")
    print(f"  bogo_sort n=20 expected shuffles: {math.factorial(20):,.0f}")
    print(f"  (At 10^9 shuffles/sec, n=20 takes ~{math.factorial(20)/1e9/3.15e7:.0f} years)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
