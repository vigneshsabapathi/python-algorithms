"""
Optimized variants of Monotonic Array check.

An array is monotonic if it is entirely non-increasing or non-decreasing.

Benchmarks three approaches using timeit.
"""

import timeit


# Variant 1: Original all() short-circuit approach
def is_monotonic_all(nums: list[int]) -> bool:
    """
    Use all() with generator — short-circuits early.
    Time: O(n), Space: O(1)

    >>> is_monotonic_all([1, 2, 2, 3])
    True
    >>> is_monotonic_all([6, 5, 4, 4])
    True
    >>> is_monotonic_all([1, 3, 2])
    False
    >>> is_monotonic_all([0])
    True
    """
    return all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)) or all(
        nums[i] >= nums[i + 1] for i in range(len(nums) - 1)
    )


# Variant 2: Single loop tracking both directions
def is_monotonic_single_loop(nums: list[int]) -> bool:
    """
    Single pass tracking increasing/decreasing flags.
    Time: O(n), Space: O(1)

    >>> is_monotonic_single_loop([1, 2, 2, 3])
    True
    >>> is_monotonic_single_loop([6, 5, 4, 4])
    True
    >>> is_monotonic_single_loop([1, 3, 2])
    False
    >>> is_monotonic_single_loop([0])
    True
    """
    increasing = decreasing = True
    for i in range(len(nums) - 1):
        if nums[i] < nums[i + 1]:
            decreasing = False
        if nums[i] > nums[i + 1]:
            increasing = False
        if not increasing and not decreasing:
            return False
    return True


# Variant 3: Using zip
def is_monotonic_zip(nums: list[int]) -> bool:
    """
    Zip-based approach pairing consecutive elements.
    Time: O(n), Space: O(1)

    >>> is_monotonic_zip([1, 2, 2, 3])
    True
    >>> is_monotonic_zip([6, 5, 4, 4])
    True
    >>> is_monotonic_zip([1, 3, 2])
    False
    >>> is_monotonic_zip([0])
    True
    """
    pairs = list(zip(nums, nums[1:]))
    return all(a <= b for a, b in pairs) or all(a >= b for a, b in pairs)


def benchmark():
    data_asc = list(range(10000))
    data_desc = list(range(10000, 0, -1))
    data_bad = list(range(5000)) + list(range(5000, 0, -1))
    n = 1000

    for label, data in [("ascending", data_asc), ("descending", data_desc), ("non-mono", data_bad)]:
        t1 = timeit.timeit(lambda: is_monotonic_all(data), number=n)
        t2 = timeit.timeit(lambda: is_monotonic_single_loop(data), number=n)
        t3 = timeit.timeit(lambda: is_monotonic_zip(data), number=n)
        print(f"[{label}]")
        print(f"  all():       {t1:.4f}s")
        print(f"  single_loop: {t2:.4f}s")
        print(f"  zip:         {t3:.4f}s")


if __name__ == "__main__":
    benchmark()
