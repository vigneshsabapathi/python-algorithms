"""
Optimized comb sort variants for interview prep.

Comb sort (Dobosiewicz 1980, Lacey & Box 1991) improves bubble sort by using
a shrinking gap > 1 so large-gap passes quickly displace turtles (small values
stuck at the end). Gap shrinks by factor 1.3 until gap = 1 (bubble sort pass).

Complexity: O(n^2) worst, O(n^2 / 2^p) in practice; ~O(n log n) on random data.
Not stable (gap > 1 swaps can cross equal elements).

Improvements:
1. Comb sort + early exit  — adds swapped flag on gap-1 passes so already-sorted
   input exits immediately instead of scanning the full array one more time.
2. Shell sort (Ciura gaps) — the "grown-up" comb sort: uses an empirically optimal
   predetermined gap sequence [701, 301, 132, 57, 23, 10, 4, 1] (Ciura 2001).
   Empirically O(n^(4/3)) to O(n^(3/2)) — significantly faster than comb on all
   input types, especially large n.
"""

from __future__ import annotations


# Ciura's empirically optimal gap sequence (2001). For n > 701 the sequence is
# extended by multiplying each term by ~2.25: 1750, 3937, 8858, ...
_CIURA_GAPS = [701, 301, 132, 57, 23, 10, 4, 1]


def comb_sort_early_exit(collection: list) -> list:
    """
    Comb sort with early-exit swapped flag on gap-1 passes.
    When gap reduces to 1 and no swap occurs the array is sorted — no need for
    another full scan.

    >>> comb_sort_early_exit([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> comb_sort_early_exit([])
    []
    >>> comb_sort_early_exit([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    >>> comb_sort_early_exit([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> comb_sort_early_exit([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> comb_sort_early_exit([3, 3, 3])
    [3, 3, 3]
    """
    arr = list(collection)
    n = len(arr)
    if n < 2:
        return arr

    gap = n
    shrink = 1.3

    while True:
        gap = max(1, int(gap / shrink))
        swapped = False
        for i in range(n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
        if gap == 1 and not swapped:
            break

    return arr


def shell_sort(collection: list) -> list:
    """
    Shell sort using Ciura's empirically optimal gap sequence.
    Each pass is an insertion sort with the current gap — elements gap apart
    are sorted relative to each other. Final gap-1 pass is plain insertion sort.

    Empirically O(n^(4/3)) on random data. Stable for gap-1 pass only; overall
    not stable (large-gap passes may reorder equal elements).

    >>> shell_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> shell_sort([])
    []
    >>> shell_sort([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    >>> shell_sort([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> shell_sort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> shell_sort([3, 3, 3])
    [3, 3, 3]
    """
    arr = list(collection)
    n = len(arr)

    # Build gap sequence: extend Ciura's list for large n
    gaps = [g for g in _CIURA_GAPS if g < n]
    if not gaps:
        gaps = [1]

    for gap in gaps:
        # Insertion sort with this gap
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp

    return arr


def benchmark() -> None:
    import random
    import timeit

    from sorts.comb_sort import comb_sort as orig

    random.seed(42)
    n_runs = 2_000

    datasets = {
        "random     n=100": random.sample(range(-500, 500), 100),
        "reversed   n=100": list(range(100, 0, -1)),
        "nearly srt n=100": list(range(98)) + [99, 98],
        "random     n=300": random.sample(range(-1500, 1500), 300),
        "random     n=1000": random.sample(range(-5000, 5000), 1000),
    }

    hdr = (
        f"{'Dataset':<22} {'original':>10} {'early-exit':>11}"
        f" {'shell':>10} {'sorted()':>10}"
    )
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        to = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        te = timeit.timeit(lambda d=data: comb_sort_early_exit(d), number=n_runs)
        ts = timeit.timeit(lambda d=data: shell_sort(d), number=n_runs)
        tq = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(
            f"{label:<22} {to:>10.3f} {te:>11.3f}"
            f" {ts:>10.3f} {tq:>10.3f}"
        )

    print()
    print("Correctness check (random n=20):")
    sample = random.sample(range(100), 20)
    expected = sorted(sample)
    for label, fn in [
        ("original", orig),
        ("early-exit", comb_sort_early_exit),
        ("shell_sort", shell_sort),
    ]:
        result = fn(list(sample))
        print(f"  {label}: correct = {result == expected}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
