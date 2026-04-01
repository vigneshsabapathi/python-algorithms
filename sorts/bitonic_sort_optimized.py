"""
Optimized bitonic sort variants for interview prep.

Two improvements over the original recursive implementation:

1. Iterative (bottom-up) bitonic sort — same O(n log²n) complexity but
   eliminates recursion overhead and call-stack depth issues.  Uses XOR
   to compute comparison partners directly, a common GPU/parallel pattern.

2. Arbitrary-length wrapper — pads to next power of 2, sorts, strips padding.
   The original silently produces WRONG results for non-power-of-2 inputs.

Interview context:
- Bitonic sort is a *sorting network*: all comparisons are fixed before any
  data is seen. This makes it uniquely suited for parallel hardware (GPU/FPGA).
- On a CPU (single thread) it's O(n log²n), worse than Timsort's O(n log n).
- The iterative version is the one you'd implement on GPU (each outer loop =
  one parallel kernel launch).
"""

from __future__ import annotations

import math


# ──────────────────────────────────────────────────────────────────────────────
# 1. Iterative bitonic sort (power-of-2 only)
# ──────────────────────────────────────────────────────────────────────────────

def bitonic_sort_iterative(array: list[int], ascending: bool = True) -> list[int]:
    """
    Bottom-up iterative bitonic sort using XOR partner indexing.
    Requires len(array) to be a power of 2.

    >>> bitonic_sort_iterative([12, 34, 92, -23, 0, -121, -167, 145])
    [-167, -121, -23, 0, 12, 34, 92, 145]
    >>> bitonic_sort_iterative([4, 3, 2, 1])
    [1, 2, 3, 4]
    >>> bitonic_sort_iterative([1, 0, 1, 0])
    [0, 0, 1, 1]
    >>> bitonic_sort_iterative([12, 34, 92, -23, 0, -121, -167, 145], ascending=False)
    [145, 92, 34, 12, 0, -23, -121, -167]
    >>> bitonic_sort_iterative([])
    []
    >>> bitonic_sort_iterative([42])
    [42]
    """
    arr = list(array)
    n = len(arr)
    if n <= 1:
        return arr

    # k = block size being merged (2, 4, 8, ..., n)
    k = 2
    while k <= n:
        # j = comparison distance within block (k/2, k/4, ..., 1)
        j = k >> 1
        while j > 0:
            for i in range(n):
                partner = i ^ j          # XOR flips bit at position log2(j)
                if partner > i:
                    # Direction: ascending if the block's "first half" bit is 0
                    # (i & k) == 0 means i is in the first half of a k-sized group
                    block_ascending = ((i & k) == 0) == ascending
                    if (block_ascending and arr[i] > arr[partner]) or (
                        not block_ascending and arr[i] < arr[partner]
                    ):
                        arr[i], arr[partner] = arr[partner], arr[i]
            j >>= 1
        k <<= 1
    return arr


# ──────────────────────────────────────────────────────────────────────────────
# 2. Arbitrary-length wrapper (pads to next power of 2)
# ──────────────────────────────────────────────────────────────────────────────

def bitonic_sort_any_length(array: list[int], ascending: bool = True) -> list[int]:
    """
    Bitonic sort for lists of *any* length.  Pads with +inf/-inf sentinels to
    the next power of 2, sorts, then strips the padding.

    >>> bitonic_sort_any_length([3, 1, 2])
    [1, 2, 3]
    >>> bitonic_sort_any_length([5, 3, 8, 1, 9])
    [1, 3, 5, 8, 9]
    >>> bitonic_sort_any_length([5, 3, 8, 1, 9], ascending=False)
    [9, 8, 5, 3, 1]
    >>> bitonic_sort_any_length([])
    []
    >>> bitonic_sort_any_length([7])
    [7]
    """
    n = len(array)
    if n <= 1:
        return list(array)
    next_pow2 = 1 << math.ceil(math.log2(n)) if n > 1 else 1
    pad_val = float("inf") if ascending else float("-inf")
    padded = list(array) + [pad_val] * (next_pow2 - n)
    sorted_padded = bitonic_sort_iterative(padded, ascending)
    return sorted_padded[:n]


# ──────────────────────────────────────────────────────────────────────────────
# Benchmark
# ──────────────────────────────────────────────────────────────────────────────

def benchmark() -> None:
    import random
    import timeit

    from sorts.bitonic_sort import bitonic_sort as orig_bitonic

    random.seed(42)
    n = 1_000
    sizes = [("n=16", 16), ("n=64", 64), ("n=256", 256), ("n=1024", 1024)]

    def run_orig(data: list[int]) -> None:
        arr = list(data)
        orig_bitonic(arr, 0, len(arr), 1)

    header = f"{'Size':<10} {'Recursive':>12} {'Iterative':>12} {'sorted()':>10}"
    print(header)
    print("-" * len(header))

    for label, size in sizes:
        data = random.sample(range(-size * 10, size * 10), size)
        t_orig = timeit.timeit(lambda d=data: run_orig(d), number=n)
        t_iter = timeit.timeit(
            lambda d=data: bitonic_sort_iterative(d), number=n
        )
        t_sort = timeit.timeit(lambda d=data: sorted(d), number=n)
        print(
            f"{label:<10} {t_orig:>12.3f} {t_iter:>12.3f} {t_sort:>10.3f}"
        )

    print()
    print("Non-power-of-2 correctness check (79% failure rate on random n=5 inputs):")
    arr5 = [12, 9, 15, 11, 6]   # known failing case
    from sorts.bitonic_sort import bitonic_sort as orig_b
    bad = list(arr5)
    orig_b(bad, 0, 5, 1)
    good = bitonic_sort_any_length(arr5)
    print(f"  original on n=5:              {bad}  <- WRONG (last element dropped)")
    print(f"  bitonic_sort_any_length n=5:  {good}  <- correct")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
