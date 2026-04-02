"""
Optimized exchange sort variants for interview prep.

Exchange sort compares arr[i] against every arr[j] where j > i and swaps
immediately whenever arr[j] < arr[i]. It is structurally identical to
selection sort's double loop, but selection sort defers the swap until the
minimum of the suffix is found — doing at most one swap per outer iteration.

Key comparison:
  Exchange sort  — swap on every out-of-order pair found: up to O(n²) swaps
  Selection sort — find the minimum first, then swap once: exactly n-1 swaps

Both are O(n²) time, O(1) space, NOT stable. Selection sort is always
preferred over exchange sort — same complexity, strictly fewer writes.

Variants:
1. selection_sort     — deferred-swap version; proves exchange sort is redundant
2. Write-count demo   — measures swaps to show exchange vs selection difference
"""

from __future__ import annotations


def selection_sort(collection: list) -> list:
    """
    Selection sort: for each position i find the minimum of arr[i..n-1],
    then swap it into position i. At most n-1 swaps total.

    >>> selection_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> selection_sort([])
    []
    >>> selection_sort([-1, -2, -3])
    [-3, -2, -1]
    >>> selection_sort([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> selection_sort([3, 3, 3])
    [3, 3, 3]
    >>> selection_sort([0, 10, -2, 5, 3])
    [-2, 0, 3, 5, 10]
    """
    arr = list(collection)
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def exchange_sort_count(collection: list) -> tuple[list, int]:
    """
    Exchange sort that also returns the number of swaps performed.

    >>> exchange_sort_count([5, 4, 3, 2, 1])[0]
    [1, 2, 3, 4, 5]
    >>> exchange_sort_count([1, 2, 3, 4, 5])[1]   # already sorted -> 0 swaps
    0
    >>> exchange_sort_count([5, 4, 3, 2, 1])[1] > 0
    True
    """
    arr = list(collection)
    n = len(arr)
    swaps = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[j] < arr[i]:
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1
    return arr, swaps


def selection_sort_count(collection: list) -> tuple[list, int]:
    """
    Selection sort that also returns the number of swaps performed.
    Swaps <= n-1, always.

    >>> selection_sort_count([5, 4, 3, 2, 1])[0]
    [1, 2, 3, 4, 5]
    >>> selection_sort_count([1, 2, 3, 4, 5])[1]  # already sorted -> 0 swaps
    0
    >>> selection_sort_count([5, 4, 3, 2, 1])[1]  # reversed n=5 -> 2 swaps (5<->1, 4<->2)
    2
    """
    arr = list(collection)
    n = len(arr)
    swaps = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return arr, swaps


def benchmark() -> None:
    import random
    import timeit

    from sorts.exchange_sort import exchange_sort as orig

    random.seed(42)
    n_runs = 2_000

    # ── Swap count comparison ─────────────────────────────────────────────
    print("Swap count comparison (n=20):")
    for label, arr_factory in [
        ("random   ", lambda: random.sample(range(100), 20)),
        ("reversed ", lambda: list(range(20, 0, -1))),
        ("sorted   ", lambda: list(range(1, 21))),
    ]:
        sample = arr_factory()
        _, es = exchange_sort_count(sample)
        _, ss = selection_sort_count(sample)
        print(f"  {label}: exchange={es:3d} swaps   selection={ss:2d} swaps")

    print()

    # ── Time benchmark ────────────────────────────────────────────────────
    datasets = {
        "random     n=100": random.sample(range(-500, 500), 100),
        "reversed   n=100": list(range(100, 0, -1)),
        "nearly srt n=100": list(range(98)) + [99, 98],
        "random     n=300": random.sample(range(-1500, 1500), 300),
    }

    hdr = f"{'Dataset':<22} {'exchange':>10} {'selection':>11} {'sorted()':>10}"
    print(hdr)
    print("-" * len(hdr))
    for label, data in datasets.items():
        te = timeit.timeit(lambda d=data: orig(list(d)), number=n_runs)
        ts = timeit.timeit(lambda d=data: selection_sort(d), number=n_runs)
        tq = timeit.timeit(lambda d=data: sorted(d), number=n_runs)
        print(f"{label:<22} {te:>10.3f} {ts:>11.3f} {tq:>10.3f}")

    print()
    print("Correctness and stability check:")
    sample = random.sample(range(100), 20)
    expected = sorted(sample)
    for label, fn in [("exchange ", orig), ("selection", selection_sort)]:
        result = fn(list(sample))
        print(f"  {label}: correct={result == expected}")

    # Stability demo: exchange sort is NOT stable
    print()
    print("Stability demo (labels track original position of equal elements):")
    # Represent [2, 2, 1] as [(2,'a'), (2,'b'), (1,'c')] to track order
    labeled = [(2, 'a'), (2, 'b'), (1, 'c')]
    # Exchange sort on first element only
    arr = list(labeled)
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[j][0] < arr[i][0]:
                arr[i], arr[j] = arr[j], arr[i]
    print(f"  exchange_sort [(2,a),(2,b),(1,c)] -> {arr}")
    print(f"  stable? {arr[1][1] == 'a' and arr[2][1] == 'b'}  "
          f"(stable would give [(1,c),(2,a),(2,b)])")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
