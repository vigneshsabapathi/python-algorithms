"""Perfect cube — variants + benchmark."""

import time
import random


def cube_float(n):
    if n < 2:
        return n >= 0
    x = int(round(abs(n) ** (1 / 3)))
    for cand in (x - 1, x, x + 1):
        if cand * cand * cand == abs(n):
            return True
    return False


def cube_binary(n):
    n = abs(n)
    lo, hi = 0, n
    while lo <= hi:
        mid = (lo + hi) // 2
        c = mid * mid * mid
        if c == n:
            return True
        if c < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def cube_newton(n):
    n = abs(n)
    if n < 2:
        return True
    x = n
    while True:
        new_x = (2 * x + n // (x * x)) // 3
        if new_x >= x:
            break
        x = new_x
    return x * x * x == n


def benchmark():
    small = [random.randint(0, 10**9) for _ in range(10_000)]
    big = [random.randint(0, 10**18) for _ in range(1000)]
    for name, fn in [("float_cbrt", cube_float), ("binary_search", cube_binary), ("newton", cube_newton)]:
        start = time.perf_counter()
        hits = sum(1 for v in small if fn(v))
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} small  hits={hits}  time={elapsed:.3f} ms")
    for name, fn in [("float_cbrt", cube_float), ("binary_search", cube_binary), ("newton", cube_newton)]:
        start = time.perf_counter()
        hits = sum(1 for v in big if fn(v))
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} big    hits={hits}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
