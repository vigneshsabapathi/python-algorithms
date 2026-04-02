"""
Radix Sort — Optimized & Alternative Implementations
=====================================================

LSD (Least Significant Digit) radix sort processes digits from right to left,
making d stable passes over the array (d = number of digits in max value).

O(n*d) time, O(n + r) space — r = radix (10 for decimal, 2 for binary).

Variants compared
-----------------
1. reference       — original: division/modulo bucketing, non-negative only
2. counting_lsd    — counting sort per digit (avoids list-of-lists allocation)
3. signed          — handles negatives via offset shift
4. base2           — binary radix (base 256 in practice) for bit manipulation
5. numpy_lsd       — vectorised per-digit counting with np.argsort
6. builtin         — sorted() for reference
"""

from __future__ import annotations

import time
import random


# ---------------------------------------------------------------------------
# 1. Reference — LSD with list-of-10-buckets per pass
# ---------------------------------------------------------------------------
def radix_sort_reference(lst: list[int]) -> list[int]:
    """
    >>> radix_sort_reference([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> radix_sort_reference([1, 100, 10, 1000])
    [1, 10, 100, 1000]
    >>> radix_sort_reference([1])
    [1]
    """
    if not lst:
        return []
    arr = lst[:]
    placement = 1
    max_val = max(arr)
    while placement <= max_val:
        buckets: list[list] = [[] for _ in range(10)]
        for v in arr:
            buckets[int((v / placement) % 10)].append(v)
        arr = [v for bucket in buckets for v in bucket]
        placement *= 10
    return arr


# ---------------------------------------------------------------------------
# 2. Counting-sort LSD — one O(n+10) counting pass per digit
#    Avoids creating 10 sublists; uses a prefix-sum array instead
# ---------------------------------------------------------------------------
def radix_sort_counting(lst: list[int]) -> list[int]:
    """
    Counting sort per digit position. O(n + 10) per pass, stable.

    >>> radix_sort_counting([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> radix_sort_counting([1, 100, 10, 1000])
    [1, 10, 100, 1000]
    >>> radix_sort_counting([])
    []
    >>> radix_sort_counting([5, 5, 5])
    [5, 5, 5]
    """
    if not lst:
        return []
    arr = lst[:]
    n = len(arr)
    exp = 1
    max_val = max(arr)
    output = [0] * n

    while exp <= max_val:
        count = [0] * 10
        for v in arr:
            count[(v // exp) % 10] += 1
        # prefix sums → starting positions
        for i in range(1, 10):
            count[i] += count[i - 1]
        # build output right-to-left (preserves stability)
        for v in reversed(arr):
            d = (v // exp) % 10
            count[d] -= 1
            output[count[d]] = v
        arr = output[:]
        exp *= 10
    return arr


# ---------------------------------------------------------------------------
# 3. Signed — handles negative integers via min-offset shift
# ---------------------------------------------------------------------------
def radix_sort_signed(lst: list[int]) -> list[int]:
    """
    Handles negative integers by shifting all values by -min so they become
    non-negative, sorting, then shifting back.

    >>> radix_sort_signed([-3, -1, 0, 2, 1])
    [-3, -1, 0, 1, 2]
    >>> radix_sort_signed([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> radix_sort_signed([])
    []
    >>> radix_sort_signed([-100, 100, 0, -50, 50])
    [-100, -50, 0, 50, 100]
    """
    if not lst:
        return []
    shift = min(lst)
    shifted = [v - shift for v in lst]
    sorted_shifted = radix_sort_counting(shifted)
    return [v + shift for v in sorted_shifted]


# ---------------------------------------------------------------------------
# 4. Base-256 LSD — 4 passes for 32-bit integers instead of ~10 passes
# ---------------------------------------------------------------------------
def radix_sort_base256(lst: list[int]) -> list[int]:
    """
    Uses base 256 (byte) radix — only 4 passes for values up to 2^32.
    Significantly fewer passes than base-10 for large values.

    >>> radix_sort_base256([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> radix_sort_base256([1, 100, 10, 1000])
    [1, 10, 100, 1000]
    >>> radix_sort_base256([])
    []
    """
    if not lst:
        return []
    arr = lst[:]
    n = len(arr)
    output = [0] * n
    BITS = 8
    BASE = 1 << BITS   # 256
    MASK = BASE - 1

    num_passes = (max(arr).bit_length() + BITS - 1) // BITS or 1
    for p in range(num_passes):
        shift = p * BITS
        count = [0] * BASE
        for v in arr:
            count[(v >> shift) & MASK] += 1
        for i in range(1, BASE):
            count[i] += count[i - 1]
        for v in reversed(arr):
            d = (v >> shift) & MASK
            count[d] -= 1
            output[count[d]] = v
        arr = output[:]
    return arr


# ---------------------------------------------------------------------------
# 5. NumPy LSD — vectorised digit extraction and argsort
# ---------------------------------------------------------------------------
def radix_sort_numpy(lst: list[int]) -> list[int]:
    """
    Vectorised: extract digits with NumPy, use stable argsort per pass.

    >>> radix_sort_numpy([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> radix_sort_numpy([1, 100, 10, 1000])
    [1, 10, 100, 1000]
    >>> radix_sort_numpy([])
    []
    """
    if not lst:
        return []
    try:
        import numpy as np
    except ImportError:
        return radix_sort_counting(lst)
    arr = np.array(lst, dtype=np.int64)
    exp = 1
    max_val = int(arr.max())
    while exp <= max_val:
        digits = (arr // exp) % 10
        order = np.argsort(digits, kind='stable')
        arr = arr[order]
        exp *= 10
    return arr.tolist()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    sizes = [1_000, 10_000, 100_000, 500_000]
    implementations = [
        ("reference",   radix_sort_reference),
        ("counting",    radix_sort_counting),
        ("base256",     radix_sort_base256),
        ("numpy",       radix_sort_numpy),
        ("sorted()",    lambda x: sorted(x)),
    ]

    for label, gen in [
        ("random [0, 10^6]",    lambda n: [random.randint(0, 1_000_000) for _ in range(n)]),
        ("random [0, 10^9]",    lambda n: [random.randint(0, 1_000_000_000) for _ in range(n)]),
        ("small range [0, 999]",lambda n: [random.randint(0, 999) for _ in range(n)]),
    ]:
        print(f"\n--- {label} ---")
        header = f"{'n':>8}  " + "  ".join(f"{name:>12}" for name, _ in implementations)
        print(header)
        print("-" * len(header))
        for n in sizes:
            data = gen(n)
            row = f"{n:>8}  "
            for _, fn in implementations:
                best = float("inf")
                for _ in range(3):
                    d = data[:]
                    t0 = time.perf_counter()
                    fn(d)
                    best = min(best, time.perf_counter() - t0)
                row += f"{best:>12.4f}  "
            print(row)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of 3 runs) ===")
    benchmark()
