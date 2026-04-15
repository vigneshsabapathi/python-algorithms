"""GCD of n numbers — variants + benchmark."""

import math
import time
import random
from functools import reduce


def gcd_euclid(a, b):
    while b:
        a, b = b, a % b
    return a


def gcd_n_loop(nums):
    g = nums[0]
    for x in nums[1:]:
        g = gcd_euclid(g, x)
        if g == 1:
            return 1
    return g


def gcd_n_reduce(nums):
    return reduce(math.gcd, nums)


def gcd_n_builtin(nums):
    return math.gcd(*nums)  # Python 3.9+


def benchmark():
    data = [random.randint(1, 10**9) * 6 for _ in range(10_000)]
    for name, fn in [
        ("loop_euclid", gcd_n_loop),
        ("reduce_math_gcd", gcd_n_reduce),
        ("math.gcd_splat", gcd_n_builtin),
    ]:
        start = time.perf_counter()
        r = fn(data)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} result={r}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
