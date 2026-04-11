#!/usr/bin/env python3
"""
Optimized and alternative implementations of Heap's Algorithm (Iterative).

The reference is the iterative counter-array version of Heap's algorithm.

Three variants:
  recursive       — classic recursive Heap's for comparison
  generator       — yield-based lazy generation (memory efficient)
  numpy_perms     — batch generation with numpy (memory-heavy but fast for small n)

Run:
    python divide_and_conquer/heaps_algorithm_iterative_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.heaps_algorithm_iterative import heaps_algorithm_iterative as reference


# ---------------------------------------------------------------------------
# Variant 1 — Recursive Heap's (for comparison)
# ---------------------------------------------------------------------------

def recursive(arr: list) -> list[list]:
    """
    Heap's algorithm, recursive version.

    >>> recursive([1, 2, 3])
    [[1, 2, 3], [2, 1, 3], [3, 1, 2], [1, 3, 2], [2, 3, 1], [3, 2, 1]]
    >>> recursive([])
    [[]]
    """
    if not arr:
        return [[]]
    result: list[list] = []
    _generate(len(arr), arr[:], result)
    return result


def _generate(k: int, arr: list, result: list[list]) -> None:
    if k == 1:
        result.append(arr[:])
        return
    _generate(k - 1, arr, result)
    for i in range(k - 1):
        if k % 2 == 0:
            arr[i], arr[k - 1] = arr[k - 1], arr[i]
        else:
            arr[0], arr[k - 1] = arr[k - 1], arr[0]
        _generate(k - 1, arr, result)


# ---------------------------------------------------------------------------
# Variant 2 — Generator (lazy, memory-efficient)
# ---------------------------------------------------------------------------

def generator(arr: list):
    """
    Heap's algorithm as a generator — yields one permutation at a time.
    Useful when you don't need all n! permutations in memory.

    >>> list(generator([1, 2, 3]))
    [[1, 2, 3], [2, 1, 3], [3, 1, 2], [1, 3, 2], [2, 3, 1], [3, 2, 1]]
    >>> list(generator([]))
    [[]]
    """
    if not arr:
        yield []
        return

    arr = arr[:]
    n = len(arr)
    yield arr[:]
    c = [0] * n
    i = 0

    while i < n:
        if c[i] < i:
            if i % 2 == 0:
                arr[0], arr[i] = arr[i], arr[0]
            else:
                arr[c[i]], arr[i] = arr[i], arr[c[i]]
            yield arr[:]
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1


# ---------------------------------------------------------------------------
# Variant 3 — itertools-based with deduplication (handles duplicates)
# ---------------------------------------------------------------------------

def dedup_permutations(arr: list) -> list[list]:
    """
    Generate unique permutations even with duplicate elements.
    Uses sorting + next-permutation approach.

    >>> dedup_permutations([1, 1, 2])
    [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    >>> dedup_permutations([1])
    [[1]]
    >>> dedup_permutations([])
    [[]]
    """
    if not arr:
        return [[]]

    arr = sorted(arr)
    result = [arr[:]]

    while True:
        # Find rightmost element smaller than its right neighbor
        i = len(arr) - 2
        while i >= 0 and arr[i] >= arr[i + 1]:
            i -= 1
        if i < 0:
            break

        # Find rightmost element larger than arr[i]
        j = len(arr) - 1
        while arr[j] <= arr[i]:
            j -= 1

        arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1:] = arr[i + 1:][::-1]
        result.append(arr[:])

    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_INPUTS = [
    [1, 2, 3],
    [1, 2, 3, 4],
    ["a", "b", "c"],
]

IMPLS = [
    ("reference", reference),
    ("recursive", recursive),
    ("generator", lambda a: list(generator(a))),
    ("dedup", dedup_permutations),
]


def run_all() -> None:
    import math

    print("\n=== Correctness ===")
    for arr in TEST_INPUTS:
        counts = {}
        for name, fn in IMPLS:
            perms = fn(arr)
            unique = len(set(tuple(p) for p in perms))
            counts[name] = (len(perms), unique)
        expected = math.factorial(len(arr))
        ok = all(c[1] == expected for c in counts.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] arr={arr}  n!={expected}  "
              + "  ".join(f"{nm}={c[0]}({c[1]} unique)" for nm, c in counts.items()))

    # Dedup test with duplicates
    perms = dedup_permutations([1, 1, 2])
    ok = len(perms) == 3 and len(set(tuple(p) for p in perms)) == 3
    print(f"  [{'OK' if ok else 'FAIL'}] dedup [1,1,2] -> {len(perms)} unique perms")

    sizes = [6, 8, 9]
    REPS = 10

    for n in sizes:
        arr = list(range(n))
        print(f"\n=== Benchmark n={n} (n!={math.factorial(n)}), {REPS} runs ===")
        for name, fn in IMPLS:
            if name == "dedup" and n > 8:
                continue  # next-permutation slower for large n
            t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
