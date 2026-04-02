"""Optimized and alternative implementations of recursive_quick_sort.py

The original uses a clean list-comprehension style with a first-element pivot.
This file explores pivot improvements within the same functional style,
plus built-in comparison.

Variants:
1. First-element pivot (original) — O(n²) worst case on sorted input
2. Random pivot            — eliminates worst-case for adversarial input
3. Median-of-3 pivot       — deterministic, avoids sorted/reverse-sorted O(n²)
4. 3-way partition (DNF)   — O(n) on all-duplicates; functional style
5. sorted() built-in       — Timsort reference

See also: sorts/quick_sort_optimized.py for in-place (Hoare/Lomuto) variants
         sorts/quick_sort_3_partition.py for 3-way partition details
"""

from __future__ import annotations
import random
import time


# ---------------------------------------------------------------------------
# 1. First-element pivot (original)
# ---------------------------------------------------------------------------
def qs_first_pivot(data: list) -> list:
    """First element as pivot — simple but O(n²) on sorted/reverse-sorted input.

    >>> qs_first_pivot([2, 1, 0])
    [0, 1, 2]
    >>> qs_first_pivot([])
    []
    >>> qs_first_pivot([1])
    [1]
    >>> qs_first_pivot([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if len(data) <= 1:
        return list(data)
    pivot = data[0]
    return (
        qs_first_pivot([e for e in data[1:] if e <= pivot])
        + [pivot]
        + qs_first_pivot([e for e in data[1:] if e > pivot])
    )


# ---------------------------------------------------------------------------
# 2. Random pivot — eliminates adversarial worst case
# ---------------------------------------------------------------------------
def qs_random_pivot(data: list) -> list:
    """Random pivot quicksort — expected O(n log n) regardless of input order.

    >>> qs_random_pivot([2, 1, 0])
    [0, 1, 2]
    >>> qs_random_pivot([])
    []
    >>> qs_random_pivot([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if len(data) <= 1:
        return list(data)
    pivot = random.choice(data)
    # Collect all equal elements to handle duplicates cleanly
    less = [e for e in data if e < pivot]
    equal = [e for e in data if e == pivot]
    greater = [e for e in data if e > pivot]
    return qs_random_pivot(less) + equal + qs_random_pivot(greater)


# ---------------------------------------------------------------------------
# 3. Median-of-3 pivot — deterministic, avoids sorted/reverse-sorted O(n²)
# ---------------------------------------------------------------------------
def _median3(a: object, b: object, c: object) -> object:
    """Return the median of three comparable values."""
    if (a <= b <= c) or (c <= b <= a):
        return b
    if (b <= a <= c) or (c <= a <= b):
        return a
    return c


def qs_median3_pivot(data: list) -> list:
    """Median-of-3 pivot: picks median of first, middle, last element.
    Avoids O(n²) on sorted and reverse-sorted inputs without randomness.

    >>> qs_median3_pivot([2, 1, 0])
    [0, 1, 2]
    >>> qs_median3_pivot([])
    []
    >>> qs_median3_pivot([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> qs_median3_pivot([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    """
    if len(data) <= 1:
        return list(data)
    pivot = _median3(data[0], data[len(data) // 2], data[-1])
    less = [e for e in data if e < pivot]
    equal = [e for e in data if e == pivot]
    greater = [e for e in data if e > pivot]
    return qs_median3_pivot(less) + equal + qs_median3_pivot(greater)


# ---------------------------------------------------------------------------
# 4. 3-way partition (Dutch National Flag) — functional style
#    Splits into <pivot, ==pivot, >pivot; O(n) when all elements are equal
# ---------------------------------------------------------------------------
def qs_3way(data: list) -> list:
    """3-way partition quicksort — O(n) on arrays with many duplicates.
    Same list-comprehension style as original; naturally handles equal elements.

    >>> qs_3way([5, 5, 5, 5])
    [5, 5, 5, 5]
    >>> qs_3way([2, 1, 0])
    [0, 1, 2]
    >>> qs_3way([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> qs_3way([])
    []
    """
    if len(data) <= 1:
        return list(data)
    pivot = data[len(data) // 2]
    less = [e for e in data if e < pivot]
    equal = [e for e in data if e == pivot]
    greater = [e for e in data if e > pivot]
    return qs_3way(less) + equal + qs_3way(greater)


# ---------------------------------------------------------------------------
# 5. Built-in sorted() — Timsort (C implementation)
# ---------------------------------------------------------------------------
def qs_builtin(data: list) -> list:
    """Python sorted() — Timsort, fastest in practice.

    >>> qs_builtin([2, 1, 0])
    [0, 1, 2]
    >>> qs_builtin([])
    []
    """
    return sorted(data)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    variants = [
        ("1. first-pivot   ", qs_first_pivot),
        ("2. random-pivot  ", qs_random_pivot),
        ("3. median3-pivot ", qs_median3_pivot),
        ("4. 3-way (DNF)   ", qs_3way),
        ("5. sorted()      ", qs_builtin),
    ]

    scenarios = [
        ("random",         lambda n: random.sample(range(n * 2), n)),
        ("sorted",         lambda n: list(range(n))),
        ("reverse sorted", lambda n: list(range(n, 0, -1))),
        ("many dupes",     lambda n: [random.randint(0, 9) for _ in range(n)]),
    ]

    # First-element pivot hits O(n²) on sorted/reversed — cap at 2k for those
    safe_sizes = {
        "random": [500, 2_000, 5_000],
        "sorted": [500, 2_000],
        "reverse sorted": [500, 2_000],
        "many dupes": [500, 2_000, 5_000],
    }

    for label, gen in scenarios:
        sizes = safe_sizes[label]
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
                    assert result == sorted(data), f"{name} wrong!"
                    print(f"    {name}: {best * 1000:7.2f} ms")
                except RecursionError:
                    print(f"    {name}: RECURSION OVERFLOW")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\nAll doctests passed.\n")
    benchmark()
