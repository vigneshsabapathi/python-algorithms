"""Wiggle Sort — optimized and alternative implementations.

Two variants of the problem:

  Wiggle Sort I  (this file's focus):
    Reorder nums so nums[0] < nums[1] > nums[2] < nums[3] ...
    Weakly-valid: equal adjacent values are acceptable at boundaries.
    O(n) one-pass solution exists.

  Wiggle Sort II (LeetCode 324 — harder):
    Same pattern but STRICT inequalities required even with duplicates.
    Requires median-finding + 3-way partition (Dutch National Flag).

Four implementations compared:
  1. One-pass adjacent swap (O(n)) — baseline, in-place
  2. Sort-then-interleave (O(n log n)) — simpler proof of correctness
  3. Wiggle Sort II — strict inequalities, handles heavy duplicates (O(n) avg)
  4. numpy vectorised interleave (O(n log n))
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Helper: validity checker (used in doctests and benchmark)
# ---------------------------------------------------------------------------

def _is_wiggle(arr: list, strict: bool = False) -> bool:
    """Return True if arr satisfies the wiggle property."""
    for i in range(1, len(arr)):
        if i % 2 == 1:  # odd index → should be > previous
            if strict and arr[i] <= arr[i - 1]:
                return False
            if not strict and arr[i] < arr[i - 1]:
                return False
        else:           # even index → should be < previous
            if strict and arr[i] >= arr[i - 1]:
                return False
            if not strict and arr[i] > arr[i - 1]:
                return False
    return True


# ---------------------------------------------------------------------------
# Approach 1: One-pass adjacent swap (baseline — same as wiggle_sort.py)
# ---------------------------------------------------------------------------

def wiggle_sort_onepass(nums: list) -> list:
    """O(n) in-place single-pass wiggle sort.

    For each index i, if the pair (nums[i-1], nums[i]) violates the required
    relationship, swap them.  Swapping adjacent elements can only fix the
    current violation without breaking any already-corrected pair.

    Note: uses Python's nums[-1] at i=0 (last element involved in first swap).
    Does NOT guarantee strict inequalities when duplicates exist.

    Examples:
        >>> wiggle_sort_onepass([3, 5, 2, 1, 6, 4])
        [3, 5, 1, 6, 2, 4]
        >>> wiggle_sort_onepass([1, 2, 3, 4, 5])
        [1, 3, 2, 5, 4]
        >>> wiggle_sort_onepass([])
        []
        >>> wiggle_sort_onepass([7, 7, 7, 7])  # all-same: no strict wiggle possible
        [7, 7, 7, 7]
    """
    for i, _ in enumerate(nums):
        if (i % 2 == 1) == (nums[i - 1] > nums[i]):
            nums[i - 1], nums[i] = nums[i], nums[i - 1]
    return nums


# ---------------------------------------------------------------------------
# Approach 2: Sort-then-interleave (O(n log n), clearest correctness proof)
# ---------------------------------------------------------------------------

def wiggle_sort_sort_interleave(nums: list) -> list:
    """Sort nums then interleave first-half (small) and second-half (large).

    After sorting: [s0, s1, ..., sk, L0, L1, ..., Lk]
    Interleaved:  [s0, L0, s1, L1, s2, L2, ...]
    Guarantees a[0] <= a[1] >= a[2] <= a[3] ... for any input.

    O(n log n) time, O(n) space.  Does NOT guarantee strict inequalities.

    Examples:
        >>> wiggle_sort_sort_interleave([3, 5, 2, 1, 6, 4])
        [1, 4, 2, 5, 3, 6]
        >>> wiggle_sort_sort_interleave([1, 2, 3, 4, 5])
        [1, 4, 2, 5, 3]
        >>> wiggle_sort_sort_interleave([])
        []
        >>> wiggle_sort_sort_interleave([1])
        [1]
    """
    s = sorted(nums)
    n = len(s)
    mid = (n + 1) // 2  # ceiling — first half is slightly larger for odd n
    result: list = [0] * n
    result[::2] = s[:mid]    # even indices ← smaller half (ascending)
    result[1::2] = s[mid:]   # odd indices  ← larger half (ascending)
    return result


# ---------------------------------------------------------------------------
# Approach 3: Wiggle Sort II — strict inequalities (LeetCode 324)
# ---------------------------------------------------------------------------

def wiggle_sort_ii(nums: list) -> list:
    """Wiggle Sort II: strict inequalities a[0] < a[1] > a[2] < a[3] ...

    Works even when the input contains heavy duplicates (e.g. [1,1,2,1,1]).
    Standard sort-then-interleave fails on such inputs because equal elements
    end up adjacent.

    Algorithm:
      1. Find the median using Python's statistics.median (or nth_element).
      2. Using a virtual index mapping (odd indices first, even second) place:
           - values > median at odd (peak) positions
           - values < median at even (valley) positions
           - median fills remaining slots
      The index mapping spreads duplicates of the median so they never sit
      next to each other, ensuring strict inequalities hold.

    Virtual index map for n elements:
        mapped(i) = (1 + 2*i) % (n | 1)
        This visits odd indices first then even indices.

    O(n) average time (median via sorting here for simplicity = O(n log n)),
    O(1) extra space (3-way partition in-place).

    Examples:
        >>> res = wiggle_sort_ii([1, 5, 1, 1, 6, 4])
        >>> _is_wiggle(res, strict=True)
        True
        >>> res = wiggle_sort_ii([1, 3, 2, 2, 3, 1])
        >>> _is_wiggle(res, strict=True)
        True
        >>> wiggle_sort_ii([])
        []
        >>> res = wiggle_sort_ii([1, 2, 3, 4, 5])
        >>> _is_wiggle(res, strict=True)
        True
    """
    if not nums:
        return nums

    n = len(nums)
    # Step 1: find median
    s = sorted(nums)
    median = s[(n - 1) // 2]

    # Step 2: 3-way partition using virtual index mapping
    # mapped(i) = (1 + 2*i) % (n | 1) visits peaks first then valleys
    def mapped(i: int) -> int:
        return (1 + 2 * i) % (n | 1)

    lo, mid_ptr, hi = 0, 0, n - 1
    while mid_ptr <= hi:
        if nums[mapped(mid_ptr)] > median:
            nums[mapped(lo)], nums[mapped(mid_ptr)] = (
                nums[mapped(mid_ptr)], nums[mapped(lo)]
            )
            lo += 1
            mid_ptr += 1
        elif nums[mapped(mid_ptr)] < median:
            nums[mapped(mid_ptr)], nums[mapped(hi)] = (
                nums[mapped(hi)], nums[mapped(mid_ptr)]
            )
            hi -= 1
        else:
            mid_ptr += 1

    return nums


# ---------------------------------------------------------------------------
# Approach 4: numpy vectorised interleave
# ---------------------------------------------------------------------------

def wiggle_sort_numpy(nums: list) -> list:
    """O(n log n) wiggle sort via numpy sort + vectorised interleave.

    Requires: pip install numpy

    Examples:
        >>> import numpy as np
        >>> res = wiggle_sort_numpy([3, 5, 2, 1, 6, 4])
        >>> _is_wiggle(res)
        True
        >>> wiggle_sort_numpy([])
        []
        >>> wiggle_sort_numpy([1])
        [1]
    """
    import numpy as np  # type: ignore[import]

    if not nums:
        return []
    a = np.sort(np.array(nums))
    n = len(a)
    mid = (n + 1) // 2
    result = np.empty(n, dtype=a.dtype)
    result[::2] = a[:mid]
    result[1::2] = a[mid:]
    return result.tolist()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare timing of all four approaches."""
    import random
    import timeit

    random.seed(42)
    n = 5000

    datasets: dict[str, list] = {
        f"random     ({n})": [random.randint(-1000, 1000) for _ in range(n)],
        f"sorted     ({n})": list(range(n)),
        f"heavy dups ({n})": [random.choice([1, 2, 3]) for _ in range(n)],
    }

    implementations: dict[str, object] = {
        "one-pass swap (O(n))":    wiggle_sort_onepass,
        "sort+interleave (O(nlogn))": wiggle_sort_sort_interleave,
        "wiggle sort II":          wiggle_sort_ii,
        "numpy interleave":        wiggle_sort_numpy,
    }

    runs = 100
    print(f"\nBenchmark — Wiggle Sort variants ({runs} runs, {n} items)\n")

    for ds_name, data in datasets.items():
        print(f"  Dataset: {ds_name}")
        print(f"  {'Implementation':<30} {'Time (ms)':>12} {'Valid':>8}")
        print("  " + "-" * 54)
        for name, fn in implementations.items():
            t = timeit.timeit(lambda fn=fn, data=data: fn(list(data)), number=runs)
            sample = fn(list(data[:20]))  # type: ignore[operator]
            valid = _is_wiggle(sample)
            print(f"  {name:<30} {t * 1000:>12.2f} {str(valid):>8}")
        print()

    # Strict-inequality correctness with heavy duplicates
    heavy = [1, 5, 1, 1, 6, 4]
    print(f"Strict-inequality test on {heavy}:")
    r1 = wiggle_sort_onepass(list(heavy))
    r2 = wiggle_sort_sort_interleave(list(heavy))
    r3 = wiggle_sort_ii(list(heavy))
    print(f"  one-pass swap:     {r1}  strict={_is_wiggle(r1, strict=True)}")
    print(f"  sort+interleave:   {r2}  strict={_is_wiggle(r2, strict=True)}")
    print(f"  wiggle sort II:    {r3}  strict={_is_wiggle(r3, strict=True)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    benchmark()
