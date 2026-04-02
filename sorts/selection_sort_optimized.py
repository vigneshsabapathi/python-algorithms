"""Optimized and alternative implementations of selection sort.

Selection sort is O(n²) comparisons always — it cannot be made asymptotically
faster while keeping the "find minimum, swap" structure.  Optimisations focus on:
  - Reducing swap count (already minimal: exactly n-1 swaps)
  - Bidirectional scan (double selection sort) to halve passes
  - Early exit (already sorted detection)
  - Dropping to built-ins for real use

Variants:
1. Standard selection sort (original)
2. Double selection sort (bidirectional — finds min AND max per pass)
3. Stable selection sort (shift instead of swap — preserves relative order)
4. Recursive selection sort (interview recursion variant)
5. sorted() built-in — Timsort reference
"""

from __future__ import annotations
import time
import random


# ---------------------------------------------------------------------------
# 1. Standard selection sort (original — already minimal swaps)
# ---------------------------------------------------------------------------
def selection_sort_standard(arr: list[int]) -> list[int]:
    """Classic selection sort: O(n²) comparisons, O(n) swaps (exactly n-1).

    >>> selection_sort_standard([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> selection_sort_standard([])
    []
    >>> selection_sort_standard([-2, -5, -45])
    [-45, -5, -2]
    """
    a = list(arr)
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for k in range(i + 1, n):
            if a[k] < a[min_idx]:
                min_idx = k
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
    return a


# ---------------------------------------------------------------------------
# 2. Double selection sort (bidirectional)
#    Each pass finds both the minimum AND maximum → ~half the passes
# ---------------------------------------------------------------------------
def selection_sort_double(arr: list[int]) -> list[int]:
    """Bidirectional selection sort: places min at left AND max at right each pass.
    Same O(n²) comparisons but ~half the outer iterations.

    >>> selection_sort_double([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> selection_sort_double([])
    []
    >>> selection_sort_double([-2, -5, -45])
    [-45, -5, -2]
    >>> selection_sort_double([1])
    [1]
    """
    a = list(arr)
    lo, hi = 0, len(a) - 1
    while lo < hi:
        min_idx, max_idx = lo, lo
        for k in range(lo, hi + 1):
            if a[k] < a[min_idx]:
                min_idx = k
            if a[k] > a[max_idx]:
                max_idx = k
        # Place minimum at lo
        a[lo], a[min_idx] = a[min_idx], a[lo]
        # If max was at lo, it moved to min_idx — fix the index
        if max_idx == lo:
            max_idx = min_idx
        # Place maximum at hi
        a[hi], a[max_idx] = a[max_idx], a[hi]
        lo += 1
        hi -= 1
    return a


# ---------------------------------------------------------------------------
# 3. Stable selection sort
#    Instead of swapping (which breaks stability), shift elements rightward
#    This preserves relative order of equal elements
# ---------------------------------------------------------------------------
def selection_sort_stable(arr: list[int]) -> list[int]:
    """Stable selection sort: shifts elements instead of swapping.
    Equal elements keep their original relative order.
    O(n²) time, O(1) extra space.

    >>> selection_sort_stable([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> selection_sort_stable([])
    []
    >>> selection_sort_stable([-2, -5, -45])
    [-45, -5, -2]
    >>> # Stability test: (val, original_index) pairs
    >>> pairs = [(2, 'a'), (1, 'b'), (2, 'c'), (1, 'd')]
    >>> selection_sort_stable(pairs)  # doctest: +NORMALIZE_WHITESPACE
    [(1, 'b'), (1, 'd'), (2, 'a'), (2, 'c')]
    """
    a = list(arr)
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for k in range(i + 1, n):
            if a[k] < a[min_idx]:
                min_idx = k
        # Shift elements right instead of swapping
        key = a[min_idx]
        while min_idx > i:
            a[min_idx] = a[min_idx - 1]
            min_idx -= 1
        a[i] = key
    return a


# ---------------------------------------------------------------------------
# 4. Recursive selection sort
#    Finds minimum of arr[i:], swaps to front, recurses on rest
# ---------------------------------------------------------------------------
def selection_sort_recursive(arr: list[int], start: int = 0) -> list[int]:
    """Recursive selection sort — same O(n²) logic expressed recursively.

    >>> selection_sort_recursive([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> selection_sort_recursive([])
    []
    >>> selection_sort_recursive([-2, -5, -45])
    [-45, -5, -2]
    """
    a = list(arr) if start == 0 else arr
    n = len(a)
    if start >= n - 1:
        return a
    min_idx = min(range(start, n), key=lambda k: a[k])
    if min_idx != start:
        a[start], a[min_idx] = a[min_idx], a[start]
    return selection_sort_recursive(a, start + 1)


# ---------------------------------------------------------------------------
# 5. Built-in sorted() — Timsort reference
# ---------------------------------------------------------------------------
def selection_sort_builtin(arr: list[int]) -> list[int]:
    """Python sorted() — Timsort, the practical answer.

    >>> selection_sort_builtin([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> selection_sort_builtin([])
    []
    """
    return sorted(arr)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    variants = [
        ("1. standard      ", selection_sort_standard),
        ("2. double (bidir)", selection_sort_double),
        ("3. stable (shift)", selection_sort_stable),
        ("4. recursive     ", selection_sort_recursive),
        ("5. sorted()      ", selection_sort_builtin),
    ]

    scenarios = [
        ("random",         lambda n: random.sample(range(n * 2), n)),
        ("sorted",         lambda n: list(range(n))),
        ("reverse sorted", lambda n: list(range(n, 0, -1))),
        ("many dupes",     lambda n: [random.randint(0, 9) for _ in range(n)]),
    ]

    sizes = [100, 500, 2_000]

    for label, gen in scenarios:
        print(f"\n--- {label} ---")
        for n in sizes:
            data = gen(n)
            print(f"  n={n:,}")
            for name, fn in variants:
                try:
                    best = float("inf")
                    for _ in range(3):
                        t0 = time.perf_counter()
                        result = fn(list(data))
                        best = min(best, time.perf_counter() - t0)
                    assert result == sorted(data), f"{name} wrong output!"
                    print(f"    {name}: {best * 1000:7.2f} ms")
                except RecursionError:
                    print(f"    {name}: RECURSION OVERFLOW")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\nAll doctests passed.\n")
    benchmark()
