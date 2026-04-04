"""Double Linear Search Recursion — fixed and optimized variants.

Three implementations:
  1. Original (buggy sentinel, RecursionError risk)
  2. Fixed recursive — uses right=-1 sentinel, no collision
  3. Iterative — no recursion limit, same logic, faster

Both recursive variants hit RecursionError for n > ~2000 (depth = n//2).
The iterative version handles any size.
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# Approach 1: Original (sentinel bug, RecursionError risk)
# ---------------------------------------------------------------------------

def search_original(list_data: list, key: int, left: int = 0, right: int = 0) -> int:
    """Original implementation — sentinel 0 collides with valid right=0.

    Examples:
        >>> search_original(list(range(11)), 5)
        5
        >>> search_original([1, 2, 4, 5, 3], 6)
        -1
        >>> search_original([], 1)
        -1
    """
    right = right or len(list_data) - 1
    if left > right:
        return -1
    elif list_data[left] == key:
        return left
    elif list_data[right] == key:
        return right
    else:
        return search_original(list_data, key, left + 1, right - 1)


# ---------------------------------------------------------------------------
# Approach 2: Fixed recursive — sentinel None avoids collision
# ---------------------------------------------------------------------------

def search_fixed(
    list_data: list, key: int, left: int = 0, right: int | None = None
) -> int:
    """Fixed recursive double linear search using None as the sentinel.

    No sentinel collision: right=None means 'uninitialized', not right=0.

    Examples:
        >>> search_fixed(list(range(11)), 5)
        5
        >>> search_fixed([1, 2, 4, 5, 3], 4)
        2
        >>> search_fixed([1, 2, 4, 5, 3], 6)
        -1
        >>> search_fixed([5], 5)
        0
        >>> search_fixed([], 1)
        -1
        >>> search_fixed([7, 8, 9], 9, 0, 0)  # explicit right=0 → only checks idx 0
        -1
    """
    if right is None:
        right = len(list_data) - 1
    if left > right:
        return -1
    if list_data[left] == key:
        return left
    if list_data[right] == key:
        return right
    return search_fixed(list_data, key, left + 1, right - 1)


# ---------------------------------------------------------------------------
# Approach 3: Iterative (no recursion limit)
# ---------------------------------------------------------------------------

def search_iterative(list_data: list, key: int) -> int:
    """Iterative double linear search — no recursion limit, same O(n) logic.

    Examples:
        >>> search_iterative(list(range(11)), 5)
        5
        >>> search_iterative([1, 2, 4, 5, 3], 4)
        2
        >>> search_iterative([1, 2, 4, 5, 3], 6)
        -1
        >>> search_iterative([5], 5)
        0
        >>> search_iterative([], 1)
        -1
    """
    left, right = 0, len(list_data) - 1
    while left <= right:
        if list_data[left] == key:
            return left
        if list_data[right] == key:
            return right
        left += 1
        right -= 1
    return -1


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    import timeit

    n = 1500  # stay under recursion limit for recursive variants
    arr = list(range(n))
    targets = {
        "near start  (idx 5)":    arr[5],
        "middle      (idx 750)":  arr[750],
        "near end    (idx 1495)": arr[1495],
        "not present":            n + 1,
    }
    impls = {
        "original (buggy sentinel)": lambda a, k: search_original(a, k),
        "fixed recursive":           lambda a, k: search_fixed(a, k),
        "iterative":                 lambda a, k: search_iterative(a, k),
        "list.index()":              lambda a, k: a.index(k) if k in a else -1,
    }
    runs = 3000
    print(f"\nBenchmark — Recursive Double Linear Search ({runs} runs, n={n})\n")
    for tgt_label, tgt in targets.items():
        print(f"  Target: {tgt_label}")
        print(f"  {'Implementation':<30} {'Time (ms)':>12} {'Result':>8}")
        print("  " + "-" * 53)
        for name, fn in impls.items():
            t = timeit.timeit(lambda fn=fn, arr=arr, tgt=tgt: fn(arr, tgt), number=runs)
            result = fn(arr, tgt)
            print(f"  {name:<30} {t * 1000:>12.2f} {str(result):>8}")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    benchmark()
