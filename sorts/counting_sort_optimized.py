"""
Optimized counting sort variants for interview prep.

Counting sort is a non-comparison, distribution sort that counts occurrences
of each value, then reconstructs the sorted array. Complexity: O(n + k) where
k = range of values (max - min + 1). Beats comparison sorts when k = O(n).

Limitations: integers only (or values mappable to integers); impractical when
k >> n (large sparse range wastes memory and time on the counting array).

Improvements:
1. Simple (accumulation) variant  — skips the prefix-sum + backward-scan
   stabilisation step; directly emits values from the count array.
   Not stable, but faster and simpler when stability is not required.
2. NumPy variant — np.bincount for non-negative integers; np.repeat to expand
   counts back to a sorted array. Vectorised, wins clearly at large n.
"""

from __future__ import annotations


def counting_sort_simple(collection: list[int]) -> list[int]:
    """
    Counting sort without the prefix-sum stabilisation step.
    Directly emits each value count times — simpler and faster than the stable
    version when the original element order does not need to be preserved.
    Not stable: equal elements always appear in ascending index order.

    >>> counting_sort_simple([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> counting_sort_simple([])
    []
    >>> counting_sort_simple([-2, -5, -45])
    [-45, -5, -2]
    >>> counting_sort_simple([3, 3, 3])
    [3, 3, 3]
    >>> counting_sort_simple([4, 3, 2, 1])
    [1, 2, 3, 4]
    """
    if not collection:
        return []

    coll_min = min(collection)
    coll_max = max(collection)
    counts = [0] * (coll_max - coll_min + 1)

    for val in collection:
        counts[val - coll_min] += 1

    return [coll_min + i for i, c in enumerate(counts) for _ in range(c)]


def counting_sort_numpy(collection: list[int]) -> list[int]:
    """
    Counting sort using NumPy's np.bincount + np.repeat.
    np.bincount counts occurrences in O(n + k) using a C loop.
    np.repeat expands the count array back to a sorted array.
    Handles non-negative integers directly; negative values are shifted.

    >>> counting_sort_numpy([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> counting_sort_numpy([])
    []
    >>> counting_sort_numpy([-2, -5, -45])
    [-45, -5, -2]
    >>> counting_sort_numpy([3, 3, 3])
    [3, 3, 3]
    >>> counting_sort_numpy([4, 3, 2, 1])
    [1, 2, 3, 4]
    """
    import numpy as np

    if not collection:
        return []

    arr = np.array(collection, dtype=np.int64)
    shift = int(arr.min())
    counts = np.bincount(arr - shift)
    return (np.repeat(np.arange(len(counts)), counts) + shift).tolist()


def benchmark() -> None:
    import random
    import timeit

    from sorts.counting_sort import counting_sort as orig

    random.seed(42)
    n_runs = 2_000

    # Counting sort only suits bounded integers; test both small-range and
    # large-range to show where it wins and loses vs sorted().
    datasets = {
        "small range n=200  k=50":  random.choices(range(50), k=200),
        "small range n=1000 k=100": random.choices(range(100), k=1000),
        "medium range n=200 k=500": random.choices(range(500), k=200),
        "large range n=200 k=10k":  random.choices(range(10_000), k=200),
    }

    hdr = (
        f"{'Dataset':<28} {'stable':>8} {'simple':>8}"
        f" {'numpy':>8} {'sorted()':>10}"
    )
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        to = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        ts = timeit.timeit(lambda d=data: counting_sort_simple(d), number=n_runs)
        tn = timeit.timeit(lambda d=data: counting_sort_numpy(d), number=n_runs)
        tq = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(
            f"{label:<28} {to:>8.3f} {ts:>8.3f}"
            f" {tn:>8.3f} {tq:>10.3f}"
        )

    print()
    print("Correctness check:")
    sample = random.choices(range(50), k=30)
    expected = sorted(sample)
    for label, fn in [
        ("stable  ", orig),
        ("simple  ", counting_sort_simple),
        ("numpy   ", counting_sort_numpy),
    ]:
        result = fn(list(sample))
        print(f"  {label}: correct = {result == expected}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
