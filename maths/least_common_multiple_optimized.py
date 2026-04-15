"""LCM — variants + benchmark."""

import math
import time
import random
from functools import reduce


def lcm_gcd(a, b):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


def lcm_n_loop(nums):
    g = 1
    for x in nums:
        g = lcm_gcd(g, x)
    return g


def lcm_n_reduce(nums):
    return reduce(math.lcm, nums)  # Python 3.9+


def lcm_n_builtin(nums):
    return math.lcm(*nums)


def benchmark():
    nums = [random.randint(1, 1000) for _ in range(5000)]
    for name, fn in [
        ("loop_gcd", lcm_n_loop),
        ("reduce_math_lcm", lcm_n_reduce),
        ("math.lcm_splat", lcm_n_builtin),
    ]:
        start = time.perf_counter()
        r = fn(nums)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} digits={len(str(r))}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
