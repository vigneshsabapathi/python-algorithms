"""Find min — variants + benchmark."""

import time
import random
from functools import reduce


def min_loop(nums):
    best = nums[0]
    for x in nums:
        if x < best:
            best = x
    return best


def min_builtin(nums):
    return min(nums)


def min_reduce(nums):
    return reduce(lambda a, b: a if a < b else b, nums)


def min_sort(nums):
    return sorted(nums)[0]


def benchmark():
    data = [random.randint(-10**6, 10**6) for _ in range(100_000)]
    for name, fn in [
        ("loop", min_loop),
        ("builtin_min", min_builtin),
        ("reduce", min_reduce),
        ("sort_first", min_sort),
    ]:
        start = time.perf_counter()
        r = fn(data)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} result={r}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
