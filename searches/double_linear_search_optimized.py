"""Double Linear Search — optimized and alternative implementations.

Five approaches compared:
  1. Double linear search (baseline) — two inward-advancing pointers
  2. Single linear search — plain left-to-right scan
  3. list.index() + try/except — C-backed, fastest in practice
  4. next() with generator — Pythonic one-liner
  5. numpy.where — vectorised C, best for large numeric arrays

Why double linear search over single?
  - Items near EITHER end are found faster.
  - Average-case: items found in ~n/4 iterations (vs n/2 for single scan).
  - Worst case: same O(n) comparisons (item in exact middle, or absent).

When to use what (interview answer):
  - Unsorted, small list, unknown position  → list.index() or next()
  - Unsorted, item likely near an end       → double linear search
  - Sorted list                             → binary search (see binary_search.py)
  - Large numeric array                     → numpy.where or numpy.searchsorted
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Approach 1: Double linear search (baseline)
# ---------------------------------------------------------------------------

def double_linear_search(array: list[int], search_item: int) -> int:
    """Two inward-advancing pointers; returns first matching index or -1.

    Examples:
        >>> double_linear_search([1, 5, 5, 10], 5)
        1
        >>> double_linear_search([1, 5, 5, 10], 100)
        -1
        >>> double_linear_search([], 1)
        -1
    """
    start_ind, end_ind = 0, len(array) - 1
    while start_ind <= end_ind:
        if array[start_ind] == search_item:
            return start_ind
        elif array[end_ind] == search_item:
            return end_ind
        else:
            start_ind += 1
            end_ind -= 1
    return -1


# ---------------------------------------------------------------------------
# Approach 2: Single linear search (left → right)
# ---------------------------------------------------------------------------

def single_linear_search(array: list[int], search_item: int) -> int:
    """Plain left-to-right scan; returns first matching index or -1.

    Examples:
        >>> single_linear_search([1, 5, 5, 10], 5)
        1
        >>> single_linear_search([1, 5, 5, 10], 100)
        -1
        >>> single_linear_search([], 1)
        -1
    """
    for i, val in enumerate(array):
        if val == search_item:
            return i
    return -1


# ---------------------------------------------------------------------------
# Approach 3: list.index() with try/except (C-backed)
# ---------------------------------------------------------------------------

def index_search(array: list[int], search_item: int) -> int:
    """list.index() wrapped in try/except — C-backed, fastest for lists.

    Examples:
        >>> index_search([1, 5, 5, 10], 5)
        1
        >>> index_search([1, 5, 5, 10], 100)
        -1
        >>> index_search([], 1)
        -1
    """
    try:
        return array.index(search_item)
    except ValueError:
        return -1


# ---------------------------------------------------------------------------
# Approach 4: next() with generator expression (Pythonic one-liner)
# ---------------------------------------------------------------------------

def next_search(array: list[int], search_item: int) -> int:
    """Generator + next(); returns first matching index or -1.

    Lazily stops as soon as the item is found — no full scan when found early.

    Examples:
        >>> next_search([1, 5, 5, 10], 5)
        1
        >>> next_search([1, 5, 5, 10], 100)
        -1
        >>> next_search([], 1)
        -1
    """
    return next((i for i, v in enumerate(array) if v == search_item), -1)


# ---------------------------------------------------------------------------
# Approach 5: numpy.where (vectorised C)
# ---------------------------------------------------------------------------

def numpy_search(array: list[int], search_item: int) -> int:
    """Vectorised search using numpy.where; returns first match index or -1.

    Best for large numeric arrays already in numpy format.
    Note: converting list→numpy adds overhead for small arrays.

    Requires: pip install numpy

    Examples:
        >>> numpy_search([1, 5, 5, 10], 5)
        1
        >>> numpy_search([1, 5, 5, 10], 100)
        -1
        >>> numpy_search([], 1)
        -1
    """
    import numpy as np  # type: ignore[import]

    arr = np.asarray(array)
    indices = np.where(arr == search_item)[0]
    return int(indices[0]) if len(indices) > 0 else -1


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare all five approaches across three search positions."""
    import random
    import timeit

    random.seed(42)
    n = 10_000
    arr = [random.randint(0, n) for _ in range(n)]

    # Three target positions: near start, middle, near end, and absent
    targets = {
        "near start  (idx ~10)":  arr[10],
        "middle      (idx ~5000)": arr[5000],
        "near end    (idx ~9990)": arr[9990],
        "not present":            n + 1,
    }

    implementations = {
        "double linear search": double_linear_search,
        "single linear search": single_linear_search,
        "list.index()":         index_search,
        "next() generator":     next_search,
        "numpy.where":          numpy_search,
    }

    runs = 2000
    print(f"\nBenchmark — Linear Search variants ({runs} runs, n={n})\n")

    for tgt_label, tgt in targets.items():
        print(f"  Target: {tgt_label}")
        print(f"  {'Implementation':<25} {'Time (ms)':>12} {'Result':>8}")
        print("  " + "-" * 48)
        for name, fn in implementations.items():
            t = timeit.timeit(lambda fn=fn, arr=arr, tgt=tgt: fn(arr, tgt), number=runs)
            result = fn(arr, tgt)
            print(f"  {name:<25} {t * 1000:>12.2f} {str(result):>8}")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    benchmark()
