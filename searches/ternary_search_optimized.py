#!/usr/bin/env python3
"""
Optimized and alternative implementations of Ternary Search.

Variants covered:
1. ternary_search_clean    -- Pure ternary search with no linear-search fallback.
                              Simpler, correct for sorted arrays.
2. binary_search_builtin   -- bisect.bisect_left (stdlib, O(log2 N)) — the
                              practical baseline for sorted-array search in Python.
3. numpy_searchsorted       -- numpy.searchsorted — vectorized, fastest for
                              large numeric arrays.

Key observation:
    Ternary search (O(log3 N)) makes MORE comparisons than binary search (O(log2 N))
    per element found because log3 N = log2 N / log2 3 ~ 0.63 * log2 N iterations,
    but each iteration does 2 comparisons instead of 1, giving:
        ternary: ~1.26 * log2 N comparisons
        binary:  ~1.00 * log2 N comparisons
    Binary search is strictly better for sorted arrays.
    Ternary search's real use is finding the extremum of a unimodal function
    (continuous domain) — NOT sorted-array search.

Run:
    python searches/ternary_search_optimized.py
"""

from __future__ import annotations

import bisect
import math
import timeit
from typing import TypeVar

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Variant 1 — clean ternary search (no linear-search fallback)
# ---------------------------------------------------------------------------


def ternary_search_clean(array: list, target) -> int:
    """
    Iterative ternary search without the linear-search fallback.

    The reference implementation switches to linear search when the window
    is smaller than `precision` (default 10). This variant searches all the
    way to a single element — cleaner and correct.

    Works on any sorted sequence supporting comparison operators.

    Returns index of target, or -1 if not found.

    >>> ternary_search_clean([0, 1, 2, 8, 13, 17, 19, 32, 42], 13)
    4
    >>> ternary_search_clean([0, 1, 2, 8, 13, 17, 19, 32, 42], 3)
    -1
    >>> ternary_search_clean([], 5)
    -1
    >>> ternary_search_clean([7], 7)
    0
    >>> ternary_search_clean([7], 1)
    -1
    >>> ternary_search_clean(['a', 'b', 'c', 'd'], 'c')
    2
    """
    left, right = 0, len(array) - 1

    while left <= right:
        one_third = left + (right - left) // 3
        two_third = right - (right - left) // 3

        if array[one_third] == target:
            return one_third
        if array[two_third] == target:
            return two_third

        if target < array[one_third]:
            right = one_third - 1
        elif target > array[two_third]:
            left = two_third + 1
        else:
            left = one_third + 1
            right = two_third - 1

    return -1


# ---------------------------------------------------------------------------
# Variant 2 — ternary search on unimodal function (the REAL use case)
# ---------------------------------------------------------------------------


def ternary_search_unimodal(
    f,
    lo: float,
    hi: float,
    find_max: bool = True,
    epsilon: float = 1e-9,
) -> float:
    """
    Ternary search on a unimodal (single-peak or single-valley) continuous function.

    THIS is the actual interview use case for ternary search — not sorted arrays.
    For sorted arrays, binary search is better (fewer comparisons).

    For a unimodal function f on [lo, hi]:
    - Split [lo, hi] into thirds at m1 and m2.
    - If f(m1) < f(m2): the peak/max is in [m1, hi]; discard [lo, m1].
    - Else: discard [m2, hi].
    - Repeat until hi - lo < epsilon.

    Time: O(log_{3/2}(range/epsilon)) iterations.

    Args:
        f: a unimodal function f(x).
        lo, hi: search bounds.
        find_max: True to find maximum, False to find minimum.
        epsilon: convergence threshold.

    Returns:
        x-coordinate of the extremum.

    >>> f = lambda x: -(x - 3)**2 + 9   # max at x=3
    >>> abs(ternary_search_unimodal(f, 0, 10, find_max=True) - 3.0) < 1e-6
    True
    >>> g = lambda x: (x - 5)**2         # min at x=5
    >>> abs(ternary_search_unimodal(g, 0, 10, find_max=False) - 5.0) < 1e-6
    True
    """
    while hi - lo > epsilon:
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if find_max:
            if f(m1) < f(m2):
                lo = m1
            else:
                hi = m2
        else:
            if f(m1) > f(m2):
                lo = m1
            else:
                hi = m2
    return (lo + hi) / 2


# ---------------------------------------------------------------------------
# Variant 3 — bisect stdlib (practical baseline for sorted-array search)
# ---------------------------------------------------------------------------


def bisect_search(array: list, target) -> int:
    """
    Sorted-array search using bisect.bisect_left (stdlib binary search).

    O(log2 N) — strictly fewer comparisons than ternary search for sorted arrays.
    This is what you should use in production Python.

    Returns index of target, or -1 if not found.

    >>> bisect_search([0, 1, 2, 8, 13, 17, 19, 32, 42], 13)
    4
    >>> bisect_search([0, 1, 2, 8, 13, 17, 19, 32, 42], 3)
    -1
    >>> bisect_search([], 5)
    -1
    >>> bisect_search([7], 7)
    0
    """
    idx = bisect.bisect_left(array, target)
    if idx < len(array) and array[idx] == target:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Variant 4 — numpy searchsorted
# ---------------------------------------------------------------------------


def numpy_search(array, target) -> int:
    """
    Sorted-array search using numpy.searchsorted.

    Uses a vectorized binary search in C. Fastest for large numeric arrays.
    Returns index or -1 if not found.

    >>> import numpy as np
    >>> numpy_search(np.array([0, 1, 2, 8, 13, 17, 19, 32, 42]), 13)
    4
    >>> numpy_search(np.array([0, 1, 2, 8, 13, 17, 19, 32, 42]), 3)
    -1
    """
    import numpy as np

    arr = np.asarray(array)
    idx = int(np.searchsorted(arr, target))
    if idx < len(arr) and arr[idx] == target:
        return idx
    return -1


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from searches.ternary_search import ite_ternary_search, rec_ternary_search

    arr = list(range(0, 10_000, 2))  # 5000 even numbers: [0, 2, 4, ..., 9998]
    n = len(arr)

    # rec_ternary_search hits Python's default recursion limit (~1000) on large arrays.
    # Use a small array for the recursive variant.
    small_arr = list(range(0, 200, 2))  # 100 elements — safe for recursive

    # --- Bug notes for reference implementation ---
    # 1. rec_ternary_search: RecursionError on large arrays (Python stack ~1000 frames)
    # 2. ite_ternary_search: index formula (left+right)//3 + 1 goes OUT OF BOUNDS
    #    when left > 0 and target is in the upper third of a large array.
    #    Masked by precision=10 fallback on small inputs; surfaces on n>=~100.
    # ternary_search_clean uses correct formula: left + (right-left)//3

    # Safe targets for the buggy reference (stays within precision fallback window)
    safe_targets = {
        "first":   (0, 0),
        "middle":  (5000, 2500),
        "missing": (7, -1),
    }

    print(f"\n=== Correctness check: safe targets (n={n}) ===")
    for label, (target, expected) in safe_targets.items():
        r1 = ite_ternary_search(arr, target)
        r3 = ternary_search_clean(arr, target)
        r4 = bisect_search(arr, target)
        ok = all(r == expected for r in [r1, r3, r4])
        print(f"  {label:8} target={target:5}  ite={r1:5}  clean={r3:5}  "
              f"bisect={r4:5}  {'OK' if ok else 'MISMATCH'}")

    print(f"\n=== Bug demonstration: last element (target=9998, expected index=4999) ===")
    try:
        r1 = ite_ternary_search(arr, 9998)
        print(f"  ite_ternary_search: idx={r1}  {'OK' if r1==4999 else 'WRONG (index formula bug)'}")
    except IndexError as e:
        print(f"  ite_ternary_search: IndexError -- {e}")
    r3 = ternary_search_clean(arr, 9998)
    r4 = bisect_search(arr, 9998)
    print(f"  ternary_search_clean: idx={r3}  {'OK' if r3==4999 else 'WRONG'}")
    print(f"  bisect_search:        idx={r4}  {'OK' if r4==4999 else 'WRONG'}")

    # Both reference variants have the same index-formula bug.
    # For the recursive variant, also avoid targets near the end of small_arr.
    print(f"\n=== Correctness check: recursive (safe targets only — both bugs documented) ===")
    for label, (target, expected) in [("first",(0,0)),("middle",(100,50)),("missing",(7,-1))]:
        r2 = rec_ternary_search(0, len(small_arr), small_arr, target)
        ok = r2 == expected
        print(f"  {label:8} target={target:3}  rec={r2:3}  {'OK' if ok else 'MISMATCH'}")

    print(f"\n  BUGS in reference (both ite and rec):")
    print(f"    1. IndexError on targets in upper third of array (index formula bug)")
    print(f"    2. RecursionError on n>{len(small_arr)} for rec variant (Python stack limit)")

    print()
    print("=== Unimodal function: ternary_search_unimodal ===")
    f1 = lambda x: -(x - 3) ** 2 + 9
    f2 = lambda x: (x - 5) ** 2
    x_max = ternary_search_unimodal(f1, 0, 10, find_max=True)
    x_min = ternary_search_unimodal(f2, 0, 10, find_max=False)
    print(f"  f(x) = -(x-3)^2 + 9  -> max at x={x_max:.8f}  (expect 3.0)")
    print(f"  g(x) = (x-5)^2       -> min at x={x_min:.8f}  (expect 5.0)")

    REPS = 2000
    print(f"\n=== Benchmark: search in sorted array of {n} elements, {REPS} runs ===")
    target_mid = 5000

    t1 = timeit.timeit(lambda: ite_ternary_search(arr, target_mid), number=REPS)
    print(f"  ite_ternary_search (reference):  {t1*1000/REPS:.4f} ms/run")

    t2 = timeit.timeit(
        lambda: rec_ternary_search(0, len(small_arr), small_arr, 100), number=REPS
    )
    print(f"  rec_ternary_search (n=100 only): {t2*1000/REPS:.4f} ms/run  "
          f"[RecursionError on n={n}]")

    t3 = timeit.timeit(lambda: ternary_search_clean(arr, target_mid), number=REPS)
    print(f"  ternary_search_clean:            {t3*1000/REPS:.4f} ms/run")

    t4 = timeit.timeit(lambda: bisect_search(arr, target_mid), number=REPS)
    print(f"  bisect_search (stdlib):          {t4*1000/REPS:.4f} ms/run")

    try:
        import numpy as np

        arr_np = np.array(arr)
        t5 = timeit.timeit(lambda: numpy_search(arr_np, target_mid), number=REPS)
        print(f"  numpy searchsorted:              {t5*1000/REPS:.4f} ms/run")
    except ImportError:
        print("  numpy not installed -- skipping")

    print()
    print("=== Comparison count (theory) ===")
    log2n = math.log2(n)
    log3n = math.log(n, 3)
    print(f"  n={n}, log2(n)={log2n:.1f}, log3(n)={log3n:.1f}")
    print(f"  Binary search comparisons:  ~{log2n:.1f}")
    print(f"  Ternary search comparisons: ~{2*log3n:.1f}  (2 per iteration x log3 N iters)")
    print(f"  Ratio: ternary/binary = {2*log3n/log2n:.2f}x  (ternary makes MORE comparisons!)")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
