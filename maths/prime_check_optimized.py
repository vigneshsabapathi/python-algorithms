"""
Prime check variants + benchmark.

1. trial_division  - check all up to sqrt(n)
2. skip_even       - skip even numbers after 2
3. six_k           - test only 6k+-1 candidates
4. miller_rabin    - deterministic Miller-Rabin for 64-bit ints
"""
from __future__ import annotations

import math
import time


def trial_division(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def skip_even(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def six_k(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    r = int(math.isqrt(n))
    while i <= r:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def miller_rabin(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # deterministic witnesses for n < 3,317,044,064,679,887,385,961,981
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def benchmark() -> None:
    targets = [97, 7919, 1000003, 10**9 + 7, 2**31 - 1, 10**18 + 9]
    funcs = [trial_division, skip_even, six_k, miller_rabin]
    print(f"{'fn':<18}{'n':>22}{'prime':>8}{'ms':>12}")
    for fn in funcs:
        for n in targets:
            if fn is trial_division and n > 10**9:
                continue
            t = time.perf_counter()
            r = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{n:>22}{str(r):>8}{dt:>12.4f}")


if __name__ == "__main__":
    benchmark()
