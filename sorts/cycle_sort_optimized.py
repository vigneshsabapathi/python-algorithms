"""
Optimized cycle sort variants for interview prep.

Cycle sort is theoretically optimal for minimising writes to storage.
Every element is written at most once to its final position — O(n) writes
total, the minimum possible for any in-place comparison sort.

This makes it valuable when writes are expensive (flash memory, EEPROM,
wear-levelled storage) even though its O(n²) comparisons mean it's slower
than Timsort on CPU benchmarks.

Variants explored:
1. Write-counting instrumented version  — proves O(n) write property
2. Write-count comparison               — cycle vs selection vs insertion
3. Benchmark (time)                     — shows where it sits among O(n²) sorts
"""

from __future__ import annotations


def cycle_sort_count_writes(array: list) -> tuple[list, int]:
    """
    Cycle sort that also returns the number of array writes performed.
    Demonstrates the O(n) theoretical minimum for in-place sorting.

    Returns (sorted_array, write_count).

    >>> cycle_sort_count_writes([4, 3, 2, 1])[0]
    [1, 2, 3, 4]
    >>> cycle_sort_count_writes([])[0]
    []
    >>> cycle_sort_count_writes([1, 2, 3, 4])[1]  # already sorted -> 0 writes
    0
    >>> cycle_sort_count_writes([4, 3, 2, 1])[1] <= 4  # at most n writes
    True
    >>> cycle_sort_count_writes([3, 3, 3])[0]
    [3, 3, 3]
    >>> cycle_sort_count_writes([-2, 5, 0, -45])[0]
    [-45, -2, 0, 5]
    """
    arr = list(array)
    n = len(arr)
    writes = 0

    for cycle_start in range(n - 1):
        item = arr[cycle_start]

        pos = cycle_start
        for i in range(cycle_start + 1, n):
            if arr[i] < item:
                pos += 1

        if pos == cycle_start:
            continue

        while item == arr[pos]:
            pos += 1

        arr[pos], item = item, arr[pos]
        writes += 1

        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if arr[i] < item:
                    pos += 1

            while item == arr[pos]:
                pos += 1

            arr[pos], item = item, arr[pos]
            writes += 1

    return arr, writes


def selection_sort_count_writes(array: list) -> tuple[list, int]:
    """
    Selection sort instrumented for write count.
    Selection sort also minimises swaps (one swap per cycle = 2 writes),
    but a swap writes 2 positions while cycle sort writes each position once.

    >>> selection_sort_count_writes([4, 3, 2, 1])[0]
    [1, 2, 3, 4]
    >>> selection_sort_count_writes([])[0]
    []
    >>> selection_sort_count_writes([1, 2, 3, 4])[1]  # already sorted -> 0 swaps
    0
    """
    arr = list(array)
    n = len(arr)
    writes = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            writes += 2  # swap = 2 writes
    return arr, writes


def insertion_sort_count_writes(array: list) -> tuple[list, int]:
    """
    Insertion sort instrumented for write count.
    Each shift is one write; insertion sort may write O(n²) times on reversed
    input (every element shifts past every other).

    >>> insertion_sort_count_writes([4, 3, 2, 1])[0]
    [1, 2, 3, 4]
    >>> insertion_sort_count_writes([])[0]
    []
    >>> insertion_sort_count_writes([1, 2, 3, 4])[1]  # sorted -> 0 writes
    0
    """
    arr = list(array)
    writes = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            writes += 1
            j -= 1
        if j + 1 != i:
            arr[j + 1] = key
            writes += 1
    return arr, writes


def benchmark() -> None:
    import random
    import timeit

    from sorts.cycle_sort import cycle_sort as orig

    random.seed(42)
    n_runs = 2_000

    # ── Write count comparison ────────────────────────────────────────────
    print("Write count comparison (n=20, random):")
    sample = random.sample(range(100), 20)
    for label, fn in [
        ("cycle_sort    ", cycle_sort_count_writes),
        ("selection_sort", selection_sort_count_writes),
        ("insertion_sort", insertion_sort_count_writes),
    ]:
        _, wc = fn(list(sample))
        print(f"  {label}: {wc} writes")

    print()
    print("Write count comparison (n=20, reversed):")
    rev = list(range(20, 0, -1))
    for label, fn in [
        ("cycle_sort    ", cycle_sort_count_writes),
        ("selection_sort", selection_sort_count_writes),
        ("insertion_sort", insertion_sort_count_writes),
    ]:
        _, wc = fn(list(rev))
        print(f"  {label}: {wc} writes")

    # ── Time benchmark ────────────────────────────────────────────────────
    print()
    datasets = {
        "random     n=100": random.sample(range(-500, 500), 100),
        "reversed   n=100": list(range(100, 0, -1)),
        "nearly srt n=100": list(range(98)) + [99, 98],
        "random     n=300": random.sample(range(-1500, 1500), 300),
    }

    hdr = f"{'Dataset':<22} {'cycle':>10} {'selection':>11} {'insertion':>11} {'sorted()':>10}"
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        tc = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        ts = timeit.timeit(
            lambda d=data: selection_sort_count_writes(d)[0], number=n_runs
        )
        ti = timeit.timeit(
            lambda d=data: insertion_sort_count_writes(d)[0], number=n_runs
        )
        tq = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(f"{label:<22} {tc:>10.3f} {ts:>11.3f} {ti:>11.3f} {tq:>10.3f}")

    print()
    print("Correctness check:")
    s = random.sample(range(100), 20)
    expected = sorted(s)
    for label, fn in [
        ("cycle_sort    ", cycle_sort_count_writes),
        ("selection_sort", selection_sort_count_writes),
        ("insertion_sort", insertion_sort_count_writes),
    ]:
        result, _ = fn(list(s))
        print(f"  {label}: correct = {result == expected}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
