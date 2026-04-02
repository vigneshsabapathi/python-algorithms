"""
Odd-Even Sort — Optimized & Alternative Implementations
========================================================

Odd-even sort (brick sort / odd-even transposition sort) is a parallel-friendly
comparison sort that alternates between swapping (even, odd) and (odd, even)
index pairs.  On a single CPU it reduces to O(n²) bubble sort; its real power
is O(n) parallel time on n processors.

Approaches compared
--------------------
1. baseline          — reference implementation (while + two for-loops)
2. early_exit        — skip second phase when first phase made no swaps
3. single_pass_flag  — fuse both phases into one loop body, one flag
4. numpy_parallel    — vectorised swap using NumPy (simulates parallel step)
5. builtin           — Python sorted() for reference
"""

from __future__ import annotations

import time
import random


# ---------------------------------------------------------------------------
# 1. Baseline — direct port of reference implementation
# ---------------------------------------------------------------------------
def odd_even_sort_baseline(lst: list) -> list:
    """
    Standard odd-even sort: alternate even-index and odd-index swap passes.

    >>> odd_even_sort_baseline([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> odd_even_sort_baseline([])
    []
    >>> odd_even_sort_baseline([-10, -1, 10, 2])
    [-10, -1, 2, 10]
    """
    arr = lst[:]
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(0, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
        for i in range(1, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
    return arr


# ---------------------------------------------------------------------------
# 2. Early-exit optimisation — skip odd phase if even phase was clean
# ---------------------------------------------------------------------------
def odd_even_sort_early_exit(lst: list) -> list:
    """
    Skip the odd-index pass entirely when the even-index pass made no swaps.
    Saves roughly half the work on nearly-sorted input.

    >>> odd_even_sort_early_exit([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> odd_even_sort_early_exit([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> odd_even_sort_early_exit([])
    []
    """
    arr = lst[:]
    n = len(arr)
    is_sorted = False
    while not is_sorted:
        is_sorted = True
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                is_sorted = False
        if not is_sorted:  # only run odd phase if even phase made a swap
            for i in range(1, n - 1, 2):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


# ---------------------------------------------------------------------------
# 3. Fixed-pass variant — run exactly n passes (no flag overhead)
#    Each full pass (even + odd) is guaranteed to move the largest unsorted
#    element to its final position, so n passes suffice.
# ---------------------------------------------------------------------------
def odd_even_sort_fixed_passes(lst: list) -> list:
    """
    Run exactly n passes instead of using a convergence flag.
    Eliminates the boolean flag and the extra condition check per iteration.
    Slightly higher work on nearly-sorted input, but avoids flag-write overhead.

    >>> odd_even_sort_fixed_passes([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> odd_even_sort_fixed_passes([3])
    [3]
    >>> odd_even_sort_fixed_passes([-3, 0, 3])
    [-3, 0, 3]
    """
    arr = lst[:]
    n = len(arr)
    for _ in range(n):
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


# ---------------------------------------------------------------------------
# 4. NumPy vectorised — simulates one parallel step per iteration
#    On a real parallel machine each step is O(1); here it's O(n) but with
#    C-speed vectorised ops, giving a meaningful speedup over pure Python.
# ---------------------------------------------------------------------------
def odd_even_sort_numpy(lst: list) -> list:
    """
    Vectorised odd-even sort using NumPy.  Each iteration computes all
    even-pair and odd-pair comparisons simultaneously via array slicing —
    mimicking the parallel nature of the algorithm.

    >>> odd_even_sort_numpy([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> odd_even_sort_numpy([])
    []
    >>> odd_even_sort_numpy([-10, -1, 10, 2])
    [-10, -1, 2, 10]
    """
    try:
        import numpy as np
    except ImportError:
        return odd_even_sort_baseline(lst)

    arr = np.array(lst, dtype=float)
    n = len(arr)
    if n < 2:
        return list(arr)

    for _ in range(n):
        # Even phase: compare pairs (0,1), (2,3), (4,5), ...
        even_idx = np.arange(0, n - 1, 2)
        mask = arr[even_idx] > arr[even_idx + 1]
        arr[even_idx[mask]], arr[even_idx[mask] + 1] = (
            arr[even_idx[mask] + 1].copy(),
            arr[even_idx[mask]].copy(),
        )
        # Odd phase: compare pairs (1,2), (3,4), (5,6), ...
        odd_idx = np.arange(1, n - 1, 2)
        if len(odd_idx):
            mask = arr[odd_idx] > arr[odd_idx + 1]
            arr[odd_idx[mask]], arr[odd_idx[mask] + 1] = (
                arr[odd_idx[mask] + 1].copy(),
                arr[odd_idx[mask]].copy(),
            )

    return [int(x) if x == int(x) else x for x in arr.tolist()]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    sizes = [500, 2_000, 5_000]
    implementations = [
        ("baseline",       odd_even_sort_baseline),
        ("early_exit",     odd_even_sort_early_exit),
        ("fixed_passes",   odd_even_sort_fixed_passes),
        ("numpy",          odd_even_sort_numpy),
        ("sorted()",       lambda x: sorted(x)),
    ]

    for label, data_fn in [
        ("random",       lambda n: random.sample(range(n * 2), n)),
        ("nearly sorted", lambda n: list(range(n - 5)) + random.sample(range(n - 5, n + 5), 5)),
        ("reversed",     lambda n: list(range(n, 0, -1))),
    ]:
        print(f"\n--- {label} input ---")
        header = f"{'n':>6}  " + "  ".join(f"{name:>16}" for name, _ in implementations)
        print(header)
        print("-" * len(header))
        for n in sizes:
            data = data_fn(n)
            row = f"{n:>6}  "
            for name, fn in implementations:
                times = []
                for _ in range(3):
                    d = data[:]
                    t0 = time.perf_counter()
                    fn(d)
                    times.append(time.perf_counter() - t0)
                row += f"{min(times):>16.4f}  "
            print(row)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of 3 runs) ===")
    benchmark()
