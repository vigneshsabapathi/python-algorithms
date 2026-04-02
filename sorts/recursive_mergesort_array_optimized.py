"""Optimized and alternative implementations of recursive merge sort on arrays.

Variants covered:
1. Classic (in-place mutation, original approach)
2. Functional (returns new sorted array, no mutation)
3. Bottom-up iterative merge sort (no recursion stack)
4. Python built-in sorted() — Timsort
5. heapq.merge() for merging two pre-sorted halves
6. Natural merge sort (exploits existing runs)
"""

from __future__ import annotations
import heapq
import time
import random


# ---------------------------------------------------------------------------
# 1. Classic — in-place mutation (original from recursive_mergesort_array.py)
# ---------------------------------------------------------------------------
def merge_sort_inplace(arr: list[int]) -> list[int]:
    """Mutates arr in-place, returns same list object.

    >>> merge_sort_inplace([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> merge_sort_inplace([])
    []
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort_inplace(left)
        merge_sort_inplace(right)
        i = j = k = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr


# ---------------------------------------------------------------------------
# 2. Functional — returns a new sorted array, original is untouched
# ---------------------------------------------------------------------------
def merge_sort_functional(arr: list[int]) -> list[int]:
    """Returns a new sorted list without modifying the input.

    >>> merge_sort_functional([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> merge_sort_functional([])
    []
    >>> original = [3, 1, 2]
    >>> _ = merge_sort_functional(original)
    >>> original  # must be unchanged
    [3, 1, 2]
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort_functional(arr[:mid])
    right = merge_sort_functional(arr[mid:])
    return _merge_two(left, right)


def _merge_two(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# 3. Bottom-up iterative merge sort — no recursion, no stack overflow risk
# ---------------------------------------------------------------------------
def merge_sort_bottom_up(arr: list[int]) -> list[int]:
    """Iterative merge sort; safe for large arrays (no recursion depth limit).

    >>> merge_sort_bottom_up([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> merge_sort_bottom_up([])
    []
    >>> merge_sort_bottom_up([1])
    [1]
    """
    n = len(arr)
    result = list(arr)
    width = 1
    while width < n:
        for i in range(0, n, width * 2):
            left = result[i : i + width]
            right = result[i + width : i + width * 2]
            merged = _merge_two(left, right)
            result[i : i + len(merged)] = merged
        width *= 2
    return result


# ---------------------------------------------------------------------------
# 4. Python built-in — Timsort (hybrid merge + insertion sort)
# ---------------------------------------------------------------------------
def merge_sort_builtin(arr: list[int]) -> list[int]:
    """Python's sorted() uses Timsort — O(n log n) worst, O(n) best for runs.

    >>> merge_sort_builtin([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> merge_sort_builtin([])
    []
    """
    return sorted(arr)


# ---------------------------------------------------------------------------
# 5. heapq.merge — merges already-sorted iterables (not a full sort)
#    Useful when you receive k pre-sorted chunks to combine.
# ---------------------------------------------------------------------------
def merge_sorted_halves_heapq(arr: list[int]) -> list[int]:
    """Splits arr in half, sorts each half, then merges with heapq.merge.
    Demonstrates heapq.merge for the k-way merge interview pattern.

    >>> merge_sorted_halves_heapq([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> merge_sorted_halves_heapq([])
    []
    """
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = sorted(arr[:mid])
    right = sorted(arr[mid:])
    return list(heapq.merge(left, right))


# ---------------------------------------------------------------------------
# 6. Natural merge sort — detects existing sorted runs (good for nearly-sorted)
# ---------------------------------------------------------------------------
def merge_sort_natural(arr: list[int]) -> list[int]:
    """Exploits existing ascending runs; O(n) on sorted input.

    >>> merge_sort_natural([5, 3, 1, 4, 2])
    [1, 2, 3, 4, 5]
    >>> merge_sort_natural([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> merge_sort_natural([])
    []
    """
    if len(arr) <= 1:
        return list(arr)

    def get_runs(a: list[int]) -> list[list[int]]:
        runs: list[list[int]] = []
        run = [a[0]]
        for x in a[1:]:
            if x >= run[-1]:
                run.append(x)
            else:
                runs.append(run)
                run = [x]
        runs.append(run)
        return runs

    runs = get_runs(arr)
    while len(runs) > 1:
        new_runs: list[list[int]] = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                new_runs.append(_merge_two(runs[i], runs[i + 1]))
            else:
                new_runs.append(runs[i])
        runs = new_runs
    return runs[0]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    sizes = [1_000, 10_000, 50_000]
    variants = [
        ("1. In-place recursive ", merge_sort_inplace),
        ("2. Functional recursive", merge_sort_functional),
        ("3. Bottom-up iterative ", merge_sort_bottom_up),
        ("4. Built-in sorted()   ", merge_sort_builtin),
        ("5. heapq.merge halves  ", merge_sorted_halves_heapq),
        ("6. Natural merge sort  ", merge_sort_natural),
    ]

    for size in sizes:
        data = random.sample(range(size * 10), size)
        print(f"\n--- n={size:,} (random) ---")
        for name, fn in variants:
            sample = list(data)
            t0 = time.perf_counter()
            result = fn(sample)
            elapsed = (time.perf_counter() - t0) * 1000
            assert result == sorted(data), f"{name} produced wrong output!"
            print(f"  {name}: {elapsed:7.2f} ms")

    # Nearly-sorted — natural merge sort should shine
    size = 10_000
    nearly = list(range(size))
    for i in range(size // 20):  # flip 5% of pairs
        a, b = random.randrange(size), random.randrange(size)
        nearly[a], nearly[b] = nearly[b], nearly[a]
    print(f"\n--- n={size:,} (nearly sorted, ~5% swaps) ---")
    for name, fn in variants:
        sample = list(nearly)
        t0 = time.perf_counter()
        fn(sample)
        elapsed = (time.perf_counter() - t0) * 1000
        print(f"  {name}: {elapsed:7.2f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\nAll doctests passed.\n")
    benchmark()
