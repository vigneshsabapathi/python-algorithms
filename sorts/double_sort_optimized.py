"""
Optimized double sort variants for interview prep.

Double sort is a bidirectional bubble sort variant: within each outer
iteration, the inner loop simultaneously pushes the smallest element left
(from the right end) and the largest element right (from the left end).
The outer loop runs ceil(n/2) times instead of n times.

Key distinction from cocktail shaker sort:
- Cocktail shaker: complete forward pass, THEN complete backward pass (sequential)
- Double sort: forward step and backward step at the same j index (interleaved)

Both are O(n²) worst/average, O(n) best, stable, in-place.

Improvements:
1. Early-exit variant  — adds swapped flag to break as soon as no swaps occur
2. Direct comparison vs cocktail shaker to clarify the structural difference
"""

from __future__ import annotations

from typing import Any


def double_sort_early_exit(collection: list[Any]) -> list[Any]:
    """
    Double sort with early-exit swapped flag.
    Breaks out of the outer loop as soon as a full outer iteration makes
    no swaps — O(n) best case on already-sorted input.

    >>> double_sort_early_exit([-1, -2, -3, -4, -5, -6, -7])
    [-7, -6, -5, -4, -3, -2, -1]
    >>> double_sort_early_exit([])
    []
    >>> double_sort_early_exit([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> double_sort_early_exit([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> double_sort_early_exit([3, 3, 3])
    [3, 3, 3]
    >>> double_sort_early_exit([-3, 10, 16, -42, 29]) == sorted([-3, 10, 16, -42, 29])
    True
    """
    arr = list(collection)
    n = len(arr)
    outer_iters = int(((n - 1) / 2) + 1)

    for _ in range(outer_iters):
        swapped = False
        for j in range(n - 1):
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
            if arr[n - 1 - j] < arr[n - 2 - j]:
                arr[n - 1 - j], arr[n - 2 - j] = arr[n - 2 - j], arr[n - 1 - j]
                swapped = True
        if not swapped:
            break

    return arr


def double_sort_vs_cocktail_demo(arr_in: list) -> dict:
    """
    Runs both double sort and cocktail shaker sort on the same input,
    counting comparisons and swaps for each. Returns a summary dict.

    >>> r = double_sort_vs_cocktail_demo([4, 3, 2, 1])
    >>> r['double_result'] == r['cocktail_result'] == [1, 2, 3, 4]
    True
    >>> r['double_result']
    [1, 2, 3, 4]
    """
    # ── Double sort with counters ─────────────────────────────────────────
    d = list(arr_in)
    n = len(d)
    d_cmps = d_swaps = 0
    for _ in range(int(((n - 1) / 2) + 1)):
        for j in range(n - 1):
            d_cmps += 2  # two comparisons per j step
            if d[j + 1] < d[j]:
                d[j], d[j + 1] = d[j + 1], d[j]
                d_swaps += 1
            if d[n - 1 - j] < d[n - 2 - j]:
                d[n - 1 - j], d[n - 2 - j] = d[n - 2 - j], d[n - 1 - j]
                d_swaps += 1

    # ── Cocktail shaker with counters ────────────────────────────────────
    c = list(arr_in)
    start, end = 0, n - 1
    c_cmps = c_swaps = 0
    while start < end:
        for i in range(start, end):
            c_cmps += 1
            if c[i] > c[i + 1]:
                c[i], c[i + 1] = c[i + 1], c[i]
                c_swaps += 1
        end -= 1
        for i in range(end, start, -1):
            c_cmps += 1
            if c[i] < c[i - 1]:
                c[i], c[i - 1] = c[i - 1], c[i]
                c_swaps += 1
        start += 1

    return {
        "double_result": d,
        "cocktail_result": c,
        "double_comparisons": d_cmps,
        "double_swaps": d_swaps,
        "cocktail_comparisons": c_cmps,
        "cocktail_swaps": c_swaps,
    }


def benchmark() -> None:
    import random
    import timeit

    from sorts.double_sort import double_sort as orig
    from sorts.cocktail_shaker_sort import cocktail_shaker_sort

    random.seed(42)
    n_runs = 2_000

    # ── Comparison/swap counts ─────────────────────────────────────────────
    print("Comparison & swap counts (n=20, random):")
    sample = random.sample(range(100), 20)
    r = double_sort_vs_cocktail_demo(sample)
    print(f"  double sort:    {r['double_comparisons']:3d} comparisons, "
          f"{r['double_swaps']:2d} swaps")
    print(f"  cocktail shaker:{r['cocktail_comparisons']:3d} comparisons, "
          f"{r['cocktail_swaps']:2d} swaps")
    print(f"  results match: {r['double_result'] == r['cocktail_result']}")

    print()
    datasets = {
        "random     n=100": random.sample(range(-500, 500), 100),
        "reversed   n=100": list(range(100, 0, -1)),
        "nearly srt n=100": list(range(98)) + [99, 98],
        "random     n=300": random.sample(range(-1500, 1500), 300),
    }

    hdr = (
        f"{'Dataset':<22} {'original':>10} {'early-exit':>11}"
        f" {'cocktail':>10} {'sorted()':>10}"
    )
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        to = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        te = timeit.timeit(lambda d=data: double_sort_early_exit(d), number=n_runs)
        tc = timeit.timeit(lambda d=data: cocktail_shaker_sort(list(d)), number=n_runs)
        tq = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(
            f"{label:<22} {to:>10.3f} {te:>11.3f}"
            f" {tc:>10.3f} {tq:>10.3f}"
        )

    print()
    print("Correctness check (random n=20):")
    s = random.sample(range(100), 20)
    expected = sorted(s)
    for label, fn in [
        ("original  ", orig),
        ("early-exit", double_sort_early_exit),
        ("cocktail  ", cocktail_shaker_sort),
    ]:
        result = fn(list(s))
        print(f"  {label}: correct = {result == expected}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
