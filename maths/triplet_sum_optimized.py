"""
Triplet sum existence — variants + benchmark.

1. brute_force     - O(n^3) triple loop
2. hash_set        - sort + outer loop + hash set, O(n^2)
3. two_pointer     - sort + two pointers, O(n^2)
"""
from __future__ import annotations

import time


def brute_force(nums, target):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == target:
                    return True
    return False


def hash_set(nums, target):
    nums = sorted(nums)
    n = len(nums)
    for i in range(n - 1):
        seen = set()
        for j in range(i + 1, n):
            if (target - nums[i] - nums[j]) in seen:
                return True
            seen.add(nums[j])
    return False


def two_pointer(nums, target):
    nums = sorted(nums)
    n = len(nums)
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == target:
                return True
            if s < target:
                lo += 1
            else:
                hi -= 1
    return False


def benchmark() -> None:
    import random

    rng = random.Random(0)
    nums = [rng.randrange(-1000, 1000) for _ in range(500)]
    target = 0
    print(f"{'fn':<14}{'result':>8}{'ms':>12}")
    for fn in (brute_force, hash_set, two_pointer):
        t = time.perf_counter()
        r = fn(nums, target)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<14}{str(r):>8}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
