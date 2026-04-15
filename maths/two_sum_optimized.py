"""
Two-sum index variants + benchmark.

1. brute_force         - O(n^2) double loop
2. hash_two_pass       - dict of values -> indices, then scan
3. hash_one_pass       - single-pass dict (canonical answer)
4. sort_and_two_ptr    - sort with original indices, then two pointer (O(n log n))
"""
from __future__ import annotations

import time


def brute_force(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return (i, j)
    return None


def hash_two_pass(nums, target):
    table = {}
    for i, x in enumerate(nums):
        table.setdefault(x, []).append(i)
    for i, x in enumerate(nums):
        comp = target - x
        if comp in table:
            for j in table[comp]:
                if j != i:
                    return (min(i, j), max(i, j))
    return None


def hash_one_pass(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        comp = target - x
        if comp in seen:
            return (seen[comp], i)
        seen[x] = i
    return None


def sort_and_two_ptr(nums, target):
    indexed = sorted(enumerate(nums), key=lambda t: t[1])
    lo, hi = 0, len(indexed) - 1
    while lo < hi:
        s = indexed[lo][1] + indexed[hi][1]
        if s == target:
            i, j = indexed[lo][0], indexed[hi][0]
            return (min(i, j), max(i, j))
        if s < target:
            lo += 1
        else:
            hi -= 1
    return None


def benchmark() -> None:
    import random

    rng = random.Random(0)
    nums = [rng.randrange(-10**6, 10**6) for _ in range(2000)]
    target = nums[100] + nums[-100]
    print(f"{'fn':<20}{'result':>14}{'ms':>12}")
    for fn in (brute_force, hash_two_pass, hash_one_pass, sort_and_two_ptr):
        t = time.perf_counter()
        for _ in range(100):
            r = fn(nums, target)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<20}{str(r):>14}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
