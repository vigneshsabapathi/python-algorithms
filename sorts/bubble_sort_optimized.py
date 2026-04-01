"""
Optimized bubble sort variants for interview prep.

Variants:
1. Last-swap optimized bubble sort — tracks position of last swap to shrink
   the unsorted window each pass, cutting unnecessary comparisons.
2. Cocktail shaker sort (bidirectional bubble) — bubbles large elements right
   AND small elements left in alternating passes. Fixes the "turtle" problem
   (small elements near the end move left very slowly in standard bubble sort).
3. sorted() — Timsort, shown for scale.

Interview insight:
- Bubble sort is O(n²) worst/average, O(n) best (already sorted).
- Cocktail shaker: same asymptotic complexity but ~2x fewer passes in practice.
- Neither beats Timsort; use sorted() for production.
- Bubble sort IS useful for detecting "nearly sorted" data (early exit).
"""

from __future__ import annotations

from typing import Any


def bubble_sort_last_swap(collection: list[Any]) -> list[Any]:
    """
    Bubble sort with last-swap position tracking.
    Each pass only scans up to where the last swap occurred — elements
    beyond that point are already in their final positions.

    >>> bubble_sort_last_swap([0, 5, 2, 3, 2])
    [0, 2, 2, 3, 5]
    >>> bubble_sort_last_swap([])
    []
    >>> bubble_sort_last_swap([-2, -45, -5])
    [-45, -5, -2]
    >>> bubble_sort_last_swap([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> bubble_sort_last_swap(['z', 'a', 'y', 'b'])
    ['a', 'b', 'y', 'z']
    """
    arr = list(collection)
    n = len(arr)
    while n > 1:
        last_swap = 0
        for i in range(n - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                last_swap = i + 1
        n = last_swap   # nothing after last_swap moved — already sorted
    return arr


def cocktail_shaker_sort(collection: list[Any]) -> list[Any]:
    """
    Bidirectional bubble sort — one pass right (bubble max to end),
    one pass left (bubble min to start). Eliminates the turtle problem:
    small elements near the end migrate left in O(n/2) passes instead of O(n).

    >>> cocktail_shaker_sort([0, 5, 2, 3, 2])
    [0, 2, 2, 3, 5]
    >>> cocktail_shaker_sort([])
    []
    >>> cocktail_shaker_sort([-2, -45, -5])
    [-45, -5, -2]
    >>> cocktail_shaker_sort([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> cocktail_shaker_sort([5, 1, 4, 2, 8, 0, 2])
    [0, 1, 2, 2, 4, 5, 8]
    >>> cocktail_shaker_sort(['z', 'a', 'y', 'b'])
    ['a', 'b', 'y', 'z']
    """
    arr = list(collection)
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        last_swap = lo
        for i in range(lo, hi):             # left -> right: bubble max up
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                last_swap = i
        hi = last_swap
        for i in range(hi, lo, -1):         # right -> left: bubble min down
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                last_swap = i
        lo = last_swap
    return arr


def benchmark() -> None:
    import random
    import timeit

    from sorts.bubble_sort import bubble_sort_iterative, bubble_sort_recursive

    random.seed(42)
    n = 2_000

    datasets = {
        "random     n=100": random.sample(range(1000), 100),
        "reversed   n=100": list(range(100, 0, -1)),
        "nearly srt n=100": list(range(98)) + [99, 98],  # turtle at end
        "random     n=300": random.sample(range(3000), 300),
    }

    hdr = f"{'Dataset':<22} {'iterative':>11} {'recursive':>11} {'last_swap':>11} {'cocktail':>11} {'sorted()':>10}"
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        ti = timeit.timeit(lambda d=data: bubble_sort_iterative(list(d)), number=n)
        tr = timeit.timeit(lambda d=data: bubble_sort_recursive(list(d)), number=n)
        tl = timeit.timeit(lambda d=data: bubble_sort_last_swap(list(d)), number=n)
        tc = timeit.timeit(lambda d=data: cocktail_shaker_sort(list(d)), number=n)
        ts = timeit.timeit(lambda d=data: sorted(d), number=n)
        print(f"{label:<22} {ti:>11.3f} {tr:>11.3f} {tl:>11.3f} {tc:>11.3f} {ts:>10.3f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
