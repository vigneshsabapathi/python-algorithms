"""Double-ended Selection Sort — optimized and alternative implementations.

Four approaches compared:
  1. Original (list-copying) — O(n^2) time, O(n) extra space
  2. In-place double-ended selection sort — O(n^2) time, O(1) extra space
  3. Numpy argsort — O(n log n), vectorised C code
  4. Python built-in sorted() — Timsort, O(n log n), highly optimised

The "original" algorithm is a double-ended selection sort: each pass pulls
the global min and max simultaneously and places them at opposite ends of
a result list.  It is O(n^2) because min/max/remove are all O(n) and the
loop runs n//2 times.

The in-place variant swaps the min/max into position without creating
extra lists, cutting constant-factor overhead (no list.remove() O(n) scan
to rebuild the backing array).
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Approach 1: Original (list-copying with min/max/remove)
# ---------------------------------------------------------------------------

def unknown_sort_original(collection: list) -> list:
    """Double-ended selection sort using list copying (baseline).

    O(n^2) time — min(), max(), remove() are each O(n); loop runs n//2 times.
    O(n) extra space for start/end accumulators.

    Examples:
        >>> unknown_sort_original([5, 3, 8, 1, 4])
        [1, 3, 4, 5, 8]
        >>> unknown_sort_original([0, 5, 3, 2, 2])
        [0, 2, 2, 3, 5]
        >>> unknown_sort_original([])
        []
        >>> unknown_sort_original([3, 3, 3])
        [3, 3, 3]
    """
    start: list = []
    end: list = []
    while len(collection) > 1:
        min_one, max_one = min(collection), max(collection)
        start.append(min_one)
        end.append(max_one)
        collection.remove(min_one)
        collection.remove(max_one)
    end.reverse()
    return start + collection + end


# ---------------------------------------------------------------------------
# Approach 2: In-place double-ended selection sort
# ---------------------------------------------------------------------------

def unknown_sort_inplace(arr: list) -> list:
    """In-place double-ended selection sort — O(n^2) time, O(1) extra space.

    Each pass scans the unsorted window [lo, hi] to find the min and max
    indices, then swaps them into position at lo and hi respectively.
    Avoids list.remove() (O(n) with element shifting) and extra allocations.

    Examples:
        >>> unknown_sort_inplace([5, 3, 8, 1, 4])
        [1, 3, 4, 5, 8]
        >>> unknown_sort_inplace([0, 5, 3, 2, 2])
        [0, 2, 2, 3, 5]
        >>> unknown_sort_inplace([])
        []
        >>> unknown_sort_inplace([3, 3, 3])
        [3, 3, 3]
        >>> unknown_sort_inplace([1])
        [1]
    """
    arr = list(arr)  # don't mutate caller's list
    lo, hi = 0, len(arr) - 1

    while lo < hi:
        min_idx = max_idx = lo
        for i in range(lo, hi + 1):
            if arr[i] < arr[min_idx]:
                min_idx = i
            if arr[i] > arr[max_idx]:
                max_idx = i

        # Place min at lo
        arr[lo], arr[min_idx] = arr[min_idx], arr[lo]

        # max_idx may have just moved because of the swap above
        if max_idx == lo:
            max_idx = min_idx

        # Place max at hi
        arr[hi], arr[max_idx] = arr[max_idx], arr[hi]

        lo += 1
        hi -= 1

    return arr


# ---------------------------------------------------------------------------
# Approach 3: numpy argsort
# ---------------------------------------------------------------------------

def unknown_sort_numpy(arr: list) -> list:
    """Sort using numpy.argsort — O(n log n) quicksort, vectorised C code.

    Requires: pip install numpy

    Examples:
        >>> unknown_sort_numpy([5, 3, 8, 1, 4])
        [1, 3, 4, 5, 8]
        >>> unknown_sort_numpy([0, 5, 3, 2, 2])
        [0, 2, 2, 3, 5]
        >>> unknown_sort_numpy([])
        []
        >>> unknown_sort_numpy([3, 3, 3])
        [3, 3, 3]
    """
    import numpy as np  # type: ignore[import]

    a = np.array(arr)
    return list(a[np.argsort(a, kind="stable")])


# ---------------------------------------------------------------------------
# Approach 4: Python built-in sorted() — Timsort
# ---------------------------------------------------------------------------

def unknown_sort_builtin(arr: list) -> list:
    """Sort using Python's built-in sorted() — Timsort, O(n log n).

    Included as the performance ceiling: any custom sort should be benchmarked
    against this.  Timsort is O(n) on already-sorted / nearly-sorted input.

    Examples:
        >>> unknown_sort_builtin([5, 3, 8, 1, 4])
        [1, 3, 4, 5, 8]
        >>> unknown_sort_builtin([0, 5, 3, 2, 2])
        [0, 2, 2, 3, 5]
        >>> unknown_sort_builtin([])
        []
        >>> unknown_sort_builtin([3, 3, 3])
        [3, 3, 3]
    """
    return sorted(arr)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare timing of all four approaches on various input shapes."""
    import random
    import timeit

    random.seed(42)
    n = 1000

    datasets: dict[str, list] = {
        f"random     ({n})": [random.randint(-500, 500) for _ in range(n)],
        f"sorted     ({n})": list(range(n)),
        f"reverse    ({n})": list(range(n, 0, -1)),
        f"all-same   ({n})": [7] * n,
    }

    implementations: dict[str, object] = {
        "original (list-copy)": unknown_sort_original,
        "in-place swap":        unknown_sort_inplace,
        "numpy argsort":        unknown_sort_numpy,
        "built-in sorted()":    unknown_sort_builtin,
    }

    runs = 50

    print(f"\nBenchmark — Double-ended Selection Sort variants ({runs} runs each)\n")

    for ds_name, data in datasets.items():
        print(f"  Dataset: {ds_name}")
        print(f"  {'Implementation':<25} {'Time (ms)':>12}")
        print("  " + "-" * 40)
        for name, fn in implementations.items():
            t = timeit.timeit(lambda fn=fn, data=data: fn(list(data)), number=runs)
            print(f"  {name:<25} {t * 1000:>12.2f}")
        print()

    # Correctness
    sample = [5, 3, 8, 1, 5, 2, 9, 3]
    expected = sorted(sample)
    print("Correctness on %s (expected %s):" % (sample, expected))
    print("  original:   %s" % unknown_sort_original(list(sample)))
    print("  in-place:   %s" % unknown_sort_inplace(sample))
    print("  numpy:      %s" % unknown_sort_numpy(sample))
    print("  builtin:    %s" % unknown_sort_builtin(sample))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    benchmark()
