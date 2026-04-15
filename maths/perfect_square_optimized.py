"""
Perfect square: multiple implementations + benchmark.

1. isqrt         - math.isqrt, fastest integer method
2. math_sqrt     - float sqrt then round (fails for very large ints)
3. binary_search - manual binary search, illustrative
4. newton        - Newton's method integer sqrt
"""
from __future__ import annotations

import math
import time


def isqrt_method(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def math_sqrt_method(n: int) -> bool:
    if n < 0:
        return False
    r = int(math.sqrt(n))
    # check neighbours to cope with float error
    for cand in (r - 1, r, r + 1):
        if cand >= 0 and cand * cand == n:
            return True
    return False


def binary_search_method(n: int) -> bool:
    if n < 0:
        return False
    lo, hi = 0, n
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == n:
            return True
        if sq < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def newton_method(n: int) -> bool:
    if n < 0:
        return False
    if n < 2:
        return True
    x = n
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x * x == n
        x = y


def benchmark() -> None:
    xs = [10**6, 10**10, 10**16, 10**30]
    funcs = [isqrt_method, math_sqrt_method, binary_search_method, newton_method]
    print(f"{'fn':<20}{'n':>34}{'result':>8}{'ms':>12}")
    for fn in funcs:
        for n in xs:
            if fn is binary_search_method and n > 10**10:
                continue
            t = time.perf_counter()
            r = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<20}{n:>34}{str(r):>8}{dt:>12.4f}")


if __name__ == "__main__":
    benchmark()
