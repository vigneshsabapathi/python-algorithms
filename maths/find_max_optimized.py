"""Find max — variants + benchmark."""

import time
import random
from functools import reduce


def max_loop(nums):
    best = nums[0]
    for x in nums:
        if x > best:
            best = x
    return best


def max_builtin(nums):
    return max(nums)


def max_reduce(nums):
    return reduce(lambda a, b: a if a > b else b, nums)


def max_sort(nums):
    return sorted(nums)[-1]


def benchmark():
    data = [random.randint(-10**6, 10**6) for _ in range(100_000)]
    for name, fn in [
        ("loop", max_loop),
        ("builtin_max", max_builtin),
        ("reduce", max_reduce),
        ("sort_last", max_sort),
    ]:
        start = time.perf_counter()
        r = fn(data)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} result={r}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
