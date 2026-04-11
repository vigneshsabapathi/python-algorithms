#!/usr/bin/env python3
"""
Optimized and alternative implementations of Heap's Algorithm.

Heap's algorithm generates all n! permutations with exactly one swap per
permutation — minimal element movement. The reference is recursive.

Three variants:
  iterative       — counter-array approach (no call stack)
  itertools_perms — stdlib itertools.permutations (C-level speed)
  sjt_algorithm   — Steinhaus-Johnson-Trotter: adjacent transpositions only

Run:
    python divide_and_conquer/heaps_algorithm_optimized.py
"""

from __future__ import annotations

import itertools
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.heaps_algorithm import heaps_algorithm as reference


# ---------------------------------------------------------------------------
# Variant 1 — Iterative Heap's (counter array)
# ---------------------------------------------------------------------------

def iterative(arr: list) -> list[list]:
    """
    Heap's algorithm, iterative version.

    >>> iterative([1, 2, 3])
    [[1, 2, 3], [2, 1, 3], [3, 1, 2], [1, 3, 2], [2, 3, 1], [3, 2, 1]]
    >>> iterative([1])
    [[1]]
    >>> iterative([])
    [[]]
    """
    n = len(arr)
    if n == 0:
        return [[]]

    arr = arr[:]
    result = [arr[:]]
    c = [0] * n
    i = 0

    while i < n:
        if c[i] < i:
            if i % 2 == 0:
                arr[0], arr[i] = arr[i], arr[0]
            else:
                arr[c[i]], arr[i] = arr[i], arr[c[i]]
            result.append(arr[:])
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1

    return result


# ---------------------------------------------------------------------------
# Variant 2 — itertools.permutations (C-level, fastest)
# ---------------------------------------------------------------------------

def itertools_perms(arr: list) -> list[list]:
    """
    Generate permutations using itertools.permutations.
    Lexicographic order (different from Heap's order).

    >>> sorted(itertools_perms([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> itertools_perms([1])
    [[1]]
    >>> itertools_perms([])
    [[]]
    """
    if not arr:
        return [[]]
    return [list(p) for p in itertools.permutations(arr)]


# ---------------------------------------------------------------------------
# Variant 3 — Steinhaus-Johnson-Trotter (adjacent transpositions)
# ---------------------------------------------------------------------------

def sjt_algorithm(arr: list) -> list[list]:
    """
    Steinhaus-Johnson-Trotter algorithm — generates permutations using
    only adjacent transpositions. Each successive permutation differs by
    swapping two adjacent elements.

    >>> perms = sjt_algorithm([1, 2, 3])
    >>> len(perms)
    6
    >>> len(set(tuple(p) for p in perms))
    6
    """
    n = len(arr)
    if n == 0:
        return [[]]

    # Each element has a direction: -1 (left) or +1 (right)
    perm = list(range(n))
    directions = [-1] * n
    result = [_get_perm(perm, arr)]

    while True:
        # Find largest mobile element
        mobile = -1
        mobile_idx = -1
        for i in range(n):
            target = i + directions[i]
            if 0 <= target < n and perm[i] > perm[target]:
                if perm[i] > mobile:
                    mobile = perm[i]
                    mobile_idx = i

        if mobile_idx == -1:
            break

        # Swap mobile element with its target
        target = mobile_idx + directions[mobile_idx]
        perm[mobile_idx], perm[target] = perm[target], perm[mobile_idx]
        directions[mobile_idx], directions[target] = directions[target], directions[mobile_idx]

        # Reverse direction of all elements larger than mobile
        for i in range(n):
            if perm[i] > mobile:
                directions[i] = -directions[i]

        result.append(_get_perm(perm, arr))

    return result


def _get_perm(perm: list[int], arr: list) -> list:
    return [arr[i] for i in perm]


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
    ("iterative", iterative),
    ("itertools", itertools_perms),
    ("sjt", sjt_algorithm),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr in TEST_INPUTS:
        counts = {}
        for name, fn in IMPLS:
            perms = fn(arr)
            unique = len(set(tuple(p) for p in perms))
            counts[name] = (len(perms), unique)
        expected = 1
        for i in range(1, len(arr) + 1):
            expected *= i
        ok = all(c[0] == expected and c[1] == expected for c in counts.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] arr={arr}  n!={expected}  "
              + "  ".join(f"{nm}={c[0]}({c[1]} unique)" for nm, c in counts.items()))

    sizes = [6, 8, 9]
    REPS = 10

    for n in sizes:
        arr = list(range(n))
        print(f"\n=== Benchmark n={n} (n!={math.factorial(n)}), {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    import math
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
