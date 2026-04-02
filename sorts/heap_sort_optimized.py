"""
Heap Sort — optimized variants for interview prep.

Heap sort: O(n log n) guaranteed, O(1) space, not stable.
Build a max-heap in O(n) via bottom-up heapify, then repeatedly extract
the max to the end of the array.

The recursive heapify in the original hits Python's recursion limit for
very deep heaps. An iterative heapify eliminates that constraint.

heapq.nlargest / heapq.nsmallest are the library answer for partial sorts.
For a full sort, sorted() (Timsort) beats heap sort in practice due to
better cache performance.

Variants:
  heap_sort_iterative: iterative sift-down (no recursion limit risk)
  heap_sort_heapq:     uses Python's heapq module (min-heap push/pop)
  heap_sort_key:       supports key= and reverse= like sorted()
"""

from __future__ import annotations

import heapq
from typing import Callable


# ---------------------------------------------------------------------------
# Variant 1: Iterative sift-down (no recursion limit)
# ---------------------------------------------------------------------------

def _sift_down(arr: list, index: int, heap_size: int) -> None:
    """Iterative max-heap sift-down from index."""
    while True:
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < heap_size and arr[left] > arr[largest]:
            largest = left
        if right < heap_size and arr[right] > arr[largest]:
            largest = right
        if largest == index:
            break
        arr[index], arr[largest] = arr[largest], arr[index]
        index = largest


def heap_sort_iterative(arr: list[int]) -> list[int]:
    """
    Heap sort with iterative sift-down.

    Identical algorithm to the recursive version but uses a while-loop
    instead of recursion, avoiding Python's default recursion limit
    (~1000) for very large inputs.

    Examples:
    >>> heap_sort_iterative([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> heap_sort_iterative([])
    []

    >>> heap_sort_iterative([-2, -5, -45])
    [-45, -5, -2]

    >>> heap_sort_iterative([4, 3, 2, 1])
    [1, 2, 3, 4]

    >>> heap_sort_iterative([1, 2, 3, 4])
    [1, 2, 3, 4]

    >>> heap_sort_iterative([3, 7, 9, 28, 123, -5, 8, -30, -200, 0, 4])
    [-200, -30, -5, 0, 3, 4, 7, 8, 9, 28, 123]
    """
    n = len(arr)
    # Build max-heap bottom-up: start at last non-leaf
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, i, n)
    # Extract max to end repeatedly
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, 0, end)
    return arr


# ---------------------------------------------------------------------------
# Variant 2: heapq-based (min-heap, library)
# ---------------------------------------------------------------------------

def heap_sort_heapq(arr: list) -> list:
    """
    Heap sort using Python's heapq module (min-heap).

    heapq.heapify is O(n); each heappop is O(log n) → O(n log n) total.
    Requires O(n) extra space (output list). heapq uses a min-heap, so
    elements come out in ascending order directly.

    In practice, use sorted() or heapq.nsmallest for production code —
    this variant shows the heapq API.

    Examples:
    >>> heap_sort_heapq([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]

    >>> heap_sort_heapq([])
    []

    >>> heap_sort_heapq([-2, -5, -45])
    [-45, -5, -2]

    >>> heap_sort_heapq([4, 3, 2, 1])
    [1, 2, 3, 4]

    >>> heap_sort_heapq([1, 2, 3, 4])
    [1, 2, 3, 4]
    """
    h = list(arr)
    heapq.heapify(h)
    return [heapq.heappop(h) for _ in range(len(h))]


# ---------------------------------------------------------------------------
# Variant 3: key= and reverse= support (like sorted())
# ---------------------------------------------------------------------------

def heap_sort_key(
    arr: list,
    key: Callable | None = None,
    reverse: bool = False,
) -> list:
    """
    Heap sort with key= and reverse= support.

    Uses heapq internally. Stores (key_value, original_value) tuples to
    avoid comparing original items when key values are equal.

    Examples:
    >>> heap_sort_key([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]

    >>> heap_sort_key(['banana', 'apple', 'cherry'], key=len)
    ['apple', 'banana', 'cherry']

    >>> heap_sort_key([3, 1, 4, 1, 5], reverse=True)
    [5, 4, 3, 1, 1]

    >>> heap_sort_key([])
    []
    """
    if key is None:
        key = lambda x: x  # noqa: E731
    # heapq is a min-heap; negate key for descending / reverse=True
    sign = -1 if reverse else 1
    h = [(sign * key(v), i, v) for i, v in enumerate(arr)]
    heapq.heapify(h)
    return [heapq.heappop(h)[2] for _ in range(len(h))]


# ---------------------------------------------------------------------------
# Reference: original recursive implementation
# ---------------------------------------------------------------------------

def _heapify_recursive(arr: list, index: int, heap_size: int) -> None:
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2
    if left < heap_size and arr[left] > arr[largest]:
        largest = left
    if right < heap_size and arr[right] > arr[largest]:
        largest = right
    if largest != index:
        arr[largest], arr[index] = arr[index], arr[largest]
        _heapify_recursive(arr, largest, heap_size)


def _heap_sort_recursive(arr: list) -> list:
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify_recursive(arr, i, n)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify_recursive(arr, 0, i)
    return arr


def benchmark() -> None:
    import copy
    import random
    import timeit

    random.seed(42)
    n = 1000
    iters = 1000

    datasets = {
        "random":        [random.randint(0, 9999) for _ in range(n)],
        "reversed":      list(range(n, 0, -1)),
        "nearly sorted": list(range(n - 10)) + [random.randint(0, n) for _ in range(10)],
        "sorted":        list(range(n)),
        "all equal":     [42] * n,
    }

    print(f"Benchmark: n={n}, {iters} iterations each\n")
    header = (f"{'Dataset':<20} {'heap_recur':>11} {'heap_iter':>10} "
              f"{'heap_heapq':>11} {'sorted()':>9}")
    print(header)
    print("-" * len(header))

    for label, data in datasets.items():
        t_r = timeit.timeit(lambda: _heap_sort_recursive(list(data)),  number=iters)
        t_i = timeit.timeit(lambda: heap_sort_iterative(list(data)),   number=iters)
        t_h = timeit.timeit(lambda: heap_sort_heapq(list(data)),       number=iters)
        t_s = timeit.timeit(lambda: sorted(data),                      number=iters)
        print(f"{label:<20} {t_r:>11.3f} {t_i:>10.3f} {t_h:>11.3f} {t_s:>9.3f}")

    # --- Stability check ---
    print("\nStability check (equal keys preserve original order):")
    data_pairs = [(2, 'a'), (2, 'b'), (1, 'c'), (1, 'd')]
    r_heap = heap_sort_heapq(copy.copy(data_pairs))
    r_key  = heap_sort_key(copy.copy(data_pairs), key=lambda x: x[0])
    r_sort = sorted(data_pairs, key=lambda x: x[0])
    print(f"  Input:           {data_pairs}")
    print(f"  heap_sort_heapq: {r_heap}  stable={r_heap == r_sort}")
    print(f"  heap_sort_key:   {r_key}  stable={r_key == r_sort}")
    print(f"  sorted():        {r_sort}  (reference)")

    # --- Partial sort: heapq.nlargest / nsmallest ---
    print("\nPartial sort (top-k) — heapq.nlargest vs sorted():")
    big = [random.randint(0, 99999) for _ in range(100_000)]
    for k in [10, 100, 1000]:
        t_nlargest = timeit.timeit(lambda: heapq.nlargest(k, big), number=100)
        t_sorted   = timeit.timeit(lambda: sorted(big, reverse=True)[:k], number=100)
        print(f"  k={k:<5}: nlargest={t_nlargest:.3f}s  sorted()={t_sorted:.3f}s  "
              f"speedup={t_sorted/t_nlargest:.1f}x")

    # --- Recursion depth demo ---
    print("\nRecursion depth: recursive heapify vs iterative on n=5000:")
    big5k = [random.randint(0, 99999) for _ in range(5000)]
    try:
        result = _heap_sort_recursive(list(big5k))
        print(f"  recursive: OK (sorted correctly: {result == sorted(big5k)})")
    except RecursionError as e:
        print(f"  recursive: RecursionError — {e}")
    result_iter = heap_sort_iterative(list(big5k))
    print(f"  iterative: OK (sorted correctly: {result_iter == sorted(big5k)})")


if __name__ == "__main__":
    benchmark()
