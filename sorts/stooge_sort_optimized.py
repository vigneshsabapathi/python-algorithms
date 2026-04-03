"""Optimized and alternative implementations of Stooge Sort.

Stooge sort is a recursive joke algorithm with O(n^2.7095) time complexity —
worse than bubble sort (O(n²)) but better than slowsort (super-polynomial).
It sorts by repeatedly sorting the first 2/3, last 2/3, then first 2/3 again.

The only "optimisation" meaningful here is understanding why it's slow and
comparing it against:
  1. Original stooge sort
  2. Stooge sort with call counter (shows recursion explosion)
  3. Bubble sort  (O(n²) — faster despite worse reputation)
  4. Insertion sort (O(n²) — adaptive, fast in practice)
  5. sorted() built-in (Timsort — the correct answer)

The recurrence: T(n) = 3·T(2n/3) + O(1)
By Master theorem (case 1): T(n) = O(n^log_{3/2}(3)) = O(n^2.7095)

Reference: https://en.wikipedia.org/wiki/Stooge_sort
"""

from __future__ import annotations
import sys
import time
import random

sys.setrecursionlimit(100_000)


# ---------------------------------------------------------------------------
# 1. Stooge sort (original)
# ---------------------------------------------------------------------------
def _stooge(arr: list, i: int, h: int) -> None:
    if i >= h:
        return
    if arr[i] > arr[h]:
        arr[i], arr[h] = arr[h], arr[i]
    if h - i + 1 > 2:
        t = (h - i + 1) // 3
        _stooge(arr, i, h - t)
        _stooge(arr, i + t, h)
        _stooge(arr, i, h - t)


def stooge_sort(arr: list) -> list:
    """Stooge sort in-place. O(n^2.7095).

    >>> stooge_sort([18.1, 0, -7.1, -1, 2, 2])
    [-7.1, -1, 0, 2, 2, 18.1]
    >>> stooge_sort([])
    []
    >>> stooge_sort([3, 1, 2])
    [1, 2, 3]
    """
    a = list(arr)
    _stooge(a, 0, len(a) - 1)
    return a


# ---------------------------------------------------------------------------
# 2. Stooge sort with call counter
# ---------------------------------------------------------------------------
def stooge_sort_counted(arr: list) -> tuple[list, int]:
    """Returns (sorted list, number of recursive calls).

    >>> result, calls = stooge_sort_counted([3, 1, 2])
    >>> result
    [1, 2, 3]
    >>> calls >= 4
    True
    """
    counter = [0]

    def _sort(a, i, h):
        counter[0] += 1
        if i >= h:
            return
        if a[i] > a[h]:
            a[i], a[h] = a[h], a[i]
        if h - i + 1 > 2:
            t = (h - i + 1) // 3
            _sort(a, i, h - t)
            _sort(a, i + t, h)
            _sort(a, i, h - t)

    a = list(arr)
    _sort(a, 0, len(a) - 1)
    return a, counter[0]


# ---------------------------------------------------------------------------
# 3. Bubble sort — O(n²), for comparison
# ---------------------------------------------------------------------------
def bubble_sort(arr: list) -> list:
    """Adaptive bubble sort — O(n) best, O(n²) worst.

    >>> bubble_sort([3, 1, 2])
    [1, 2, 3]
    >>> bubble_sort([])
    []
    """
    a = list(arr)
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


# ---------------------------------------------------------------------------
# 4. Insertion sort — O(n²) but adaptive and fast in practice
# ---------------------------------------------------------------------------
def insertion_sort(arr: list) -> list:
    """Insertion sort — O(n) best, O(n²) worst, stable.

    >>> insertion_sort([3, 1, 2])
    [1, 2, 3]
    >>> insertion_sort([])
    []
    """
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


# ---------------------------------------------------------------------------
# 5. Built-in sorted() — Timsort
# ---------------------------------------------------------------------------
def sort_builtin(arr: list) -> list:
    """Python sorted() — Timsort, O(n log n).

    >>> sort_builtin([3, 1, 2])
    [1, 2, 3]
    >>> sort_builtin([])
    []
    """
    return sorted(arr)


# ---------------------------------------------------------------------------
# Recursion call count table — show the O(n^2.7) explosion
# ---------------------------------------------------------------------------
def show_call_counts() -> None:
    print("Stooge sort recursive call counts:")
    print(f"  {'n':>4}  {'calls':>10}  {'n²':>10}  {'n^2.71':>10}  {'ratio/n²':>10}")
    for n in [3, 5, 8, 10, 15, 20, 25, 30]:
        data = list(range(n, 0, -1))  # reverse sorted — most work
        _, calls = stooge_sort_counted(data)
        n2 = n ** 2
        n271 = n ** 2.7095
        print(f"  {n:>4}  {calls:>10,}  {n2:>10,}  {n271:>10.0f}  {calls/n2:>10.2f}x")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    variants = [
        ("stooge sort    ", stooge_sort),
        ("bubble sort    ", bubble_sort),
        ("insertion sort ", insertion_sort),
        ("sorted()       ", sort_builtin),
    ]

    scenarios = [
        ("random",         lambda n: random.sample(range(n * 2), n)),
        ("sorted",         lambda n: list(range(n))),
        ("reverse sorted", lambda n: list(range(n, 0, -1))),
    ]

    # Stooge sort hits recursion limit / takes very long beyond ~300
    sizes = [10, 30, 50, 100, 200]

    for label, gen in scenarios:
        print(f"\n--- {label} ---")
        for n in sizes:
            data = gen(n)
            print(f"  n={n}")
            for name, fn in variants:
                try:
                    best = float("inf")
                    for _ in range(3):
                        t0 = time.perf_counter()
                        result = fn(list(data))
                        best = min(best, time.perf_counter() - t0)
                    assert result == sorted(data), f"{name} wrong!"
                    print(f"    {name}: {best * 1000:8.3f} ms")
                except RecursionError:
                    print(f"    {name}: RECURSION OVERFLOW")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("All doctests passed.\n")
    show_call_counts()
    print()
    benchmark()
