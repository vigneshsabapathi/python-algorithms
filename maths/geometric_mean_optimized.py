"""Geometric mean — variants + benchmark."""

import math
import time
import random
import statistics


def gm_product(nums):
    p = 1.0
    for x in nums:
        p *= x
    return p ** (1 / len(nums))


def gm_log_sum(nums):
    return math.exp(sum(math.log(x) for x in nums) / len(nums))


def gm_statistics(nums):
    return statistics.geometric_mean(nums)


def benchmark():
    data = [random.uniform(0.5, 5.0) for _ in range(10_000)]
    for name, fn in [
        ("direct_product", gm_product),
        ("log_sum_exp", gm_log_sum),
        ("statistics.gm", gm_statistics),
    ]:
        start = time.perf_counter()
        r = fn(data)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} result={r:.6f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
