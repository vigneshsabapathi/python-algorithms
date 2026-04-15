"""
3SUM variants + benchmark.

1. brute_force      - O(n^3) triple loop
2. hash_complement  - O(n^2) outer + O(1) lookup per pair
3. two_pointer      - sort + two pointers, O(n^2)
"""
from __future__ import annotations

import time
from typing import List


def brute_force(nums):
    nums = sorted(nums)
    n = len(nums)
    seen = set()
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    t = (nums[i], nums[j], nums[k])
                    if t not in seen:
                        seen.add(t)
                        out.append(list(t))
    return out


def hash_complement(nums):
    nums = sorted(nums)
    n = len(nums)
    out = set()
    for i in range(n - 2):
        seen = set()
        for j in range(i + 1, n):
            target = -nums[i] - nums[j]
            if target in seen:
                out.add((nums[i], target, nums[j]))
            seen.add(nums[j])
    return [list(t) for t in sorted(out)]


def two_pointer(nums):
    nums = sorted(nums)
    n = len(nums)
    out = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                out.append([nums[i], nums[lo], nums[hi]])
                lo += 1; hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return out


def benchmark() -> None:
    import random

    rng = random.Random(0)
    nums = [rng.randrange(-50, 50) for _ in range(200)]
    print(f"{'fn':<18}{'count':>10}{'ms':>12}")
    for fn in (brute_force, hash_complement, two_pointer):
        t = time.perf_counter()
        r = fn(nums)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<18}{len(r):>10}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
