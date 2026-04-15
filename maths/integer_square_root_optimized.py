"""Integer square root — variants + benchmark."""

import math
import time
import random


def isqrt_newton(n):
    if n < 2:
        return n
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def isqrt_binary(n):
    if n < 2:
        return n
    lo, hi = 1, n
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= n < (mid + 1) * (mid + 1):
            return mid
        if mid * mid > n:
            hi = mid - 1
        else:
            lo = mid + 1
    return lo


def isqrt_math(n):
    return math.isqrt(n)


def isqrt_float(n):
    # Fast but unsafe for huge n (float precision)
    return int(n**0.5)


def benchmark():
    data = [random.randint(1, 10**18) for _ in range(5000)]
    for name, fn in [
        ("newton", isqrt_newton),
        ("binary_search", isqrt_binary),
        ("math.isqrt", isqrt_math),
        ("float_cast", isqrt_float),
    ]:
        start = time.perf_counter()
        for v in data:
            fn(v)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
