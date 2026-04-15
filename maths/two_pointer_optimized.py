"""
Two-pointer pair-sum — variants + benchmark.

1. two_pointer     - sort + two pointers, O(n) after sort
2. hash_set        - O(n) pass with set; works on unsorted
3. binary_search   - sort + for each i bsearch target-nums[i], O(n log n)
"""
from __future__ import annotations

import bisect
import time


def two_pointer(nums, target):
    nums = sorted(nums)
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return (nums[lo], nums[hi])
        if s < target:
            lo += 1
        else:
            hi -= 1
    return None


def hash_set(nums, target):
    seen = set()
    for x in nums:
        if (target - x) in seen:
            return (target - x, x)
        seen.add(x)
    return None


def binary_search(nums, target):
    nums = sorted(nums)
    for i, x in enumerate(nums):
        j = bisect.bisect_left(nums, target - x, i + 1)
        if j < len(nums) and nums[j] == target - x:
            return (x, target - x)
    return None


def benchmark() -> None:
    import random

    rng = random.Random(0)
    nums = [rng.randrange(0, 10**6) for _ in range(50_000)]
    nums.sort()
    t_target = nums[100] + nums[-100]
    print(f"{'fn':<16}{'pair':>20}{'ms':>12}")
    for fn in (two_pointer, hash_set, binary_search):
        t = time.perf_counter()
        for _ in range(10):
            r = fn(nums, t_target)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<16}{str(r):>20}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
