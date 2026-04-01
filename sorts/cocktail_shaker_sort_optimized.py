"""
Optimized cocktail shaker sort variants for interview prep.

Cocktail shaker sort (a.k.a. bidirectional bubble sort) fixes bubble sort's
"turtle problem" by also bubbling small elements leftward on reverse passes.
Complexity: O(n^2) worst/average, O(n) best (already sorted). Stable.

Improvements:
1. Last-swap optimization  — shrink active window each pass (fewer comparisons)
2. Comb sort              — uses shrinking gap > 1 to break up turtles faster,
                            achieves O(n^2 / 2^p) in practice, ~10x faster than
                            cocktail on random data
3. Comparison with sorted() to illustrate the practical gap.
"""

from __future__ import annotations


def cocktail_shaker_last_swap(collection: list) -> list:
    """
    Cocktail shaker sort with last-swap boundary tracking.
    After each half-pass the active region shrinks to the last swap position,
    skipping elements already in their final place.

    >>> cocktail_shaker_last_swap([4, 5, 2, 1, 2])
    [1, 2, 2, 4, 5]
    >>> cocktail_shaker_last_swap([])
    []
    >>> cocktail_shaker_last_swap([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    >>> cocktail_shaker_last_swap([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> cocktail_shaker_last_swap([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> cocktail_shaker_last_swap([3, 3, 3])
    [3, 3, 3]
    """
    arr = list(collection)
    start, end = 0, len(arr) - 1

    while start < end:
        new_end = start
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                new_end = i
        end = new_end
        if start >= end:
            break

        new_start = end
        for i in range(end, start, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
                new_start = i
        start = new_start

    return arr


def comb_sort(collection: list) -> list:
    """
    Comb sort: like bubble sort but uses a shrinking gap > 1 to move turtles
    quickly. Gap starts at len(arr) and shrinks by factor 1/1.3 each pass.
    When gap = 1 it degenerates to bubble sort for a final cleanup pass.

    Average: O(n^2 / 2^p) where p = number of increments.
    Typical practice: ~O(n log n) on random data; worst O(n^2) still possible.
    Not stable (gap > 1 swaps can cross equal elements).

    >>> comb_sort([4, 5, 2, 1, 2])
    [1, 2, 2, 4, 5]
    >>> comb_sort([])
    []
    >>> comb_sort([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    >>> comb_sort([1, 2, 3, 4])
    [1, 2, 3, 4]
    >>> comb_sort([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> comb_sort([3, 3, 3])
    [3, 3, 3]
    """
    arr = list(collection)
    n = len(arr)
    if n < 2:
        return arr

    gap = n
    shrink = 1.3
    sorted_ = False

    while not sorted_:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_ = True  # assume sorted; a swap will reset this

        i = 0
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_ = False
            i += 1

    return arr


def benchmark() -> None:
    import random
    import timeit

    from sorts.cocktail_shaker_sort import cocktail_shaker_sort as orig

    random.seed(42)
    n_runs = 2_000

    datasets = {
        "random     n=100": random.sample(range(-500, 500), 100),
        "reversed   n=100": list(range(100, 0, -1)),
        "nearly srt n=100": list(range(98)) + [99, 98],
        "random     n=300": random.sample(range(-1500, 1500), 300),
    }

    hdr = (
        f"{'Dataset':<22} {'original':>10} {'last-swap':>10}"
        f" {'comb':>10} {'sorted()':>10}"
    )
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        to = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        tl = timeit.timeit(
            lambda d=data: cocktail_shaker_last_swap(d), number=n_runs
        )
        tc = timeit.timeit(lambda d=data: comb_sort(d), number=n_runs)
        ts = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(
            f"{label:<22} {to:>10.3f} {tl:>10.3f}"
            f" {tc:>10.3f} {ts:>10.3f}"
        )

    print()
    print("Correctness check (random n=20):")
    sample = random.sample(range(100), 20)
    expected = sorted(sample)
    for label, fn in [
        ("original", orig),
        ("last-swap", cocktail_shaker_last_swap),
        ("comb_sort", comb_sort),
    ]:
        result = fn(list(sample))
        print(f"  {label}: correct = {result == expected}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
