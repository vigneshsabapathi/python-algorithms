"""
Pollard's rho variants + benchmark against trial division.

1. trial_division    - check primes up to sqrt(n)
2. pollard_floyd     - classic Floyd tortoise/hare cycle detection
3. pollard_brent     - Brent's improvement (fewer gcd calls)
"""
from __future__ import annotations

import math
import random
import time


def trial_division(n: int) -> int | None:
    if n % 2 == 0:
        return 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i
        i += 2
    return None


def pollard_floyd(n: int, seed: int = 2) -> int | None:
    if n % 2 == 0:
        return 2
    rng = random.Random(seed)
    for _ in range(20):
        x = rng.randrange(2, n)
        y = x
        c = rng.randrange(1, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d
    return None


def pollard_brent(n: int, seed: int = 2) -> int | None:
    if n % 2 == 0:
        return 2
    rng = random.Random(seed)
    for _ in range(20):
        y, c, m = rng.randrange(1, n), rng.randrange(1, n), rng.randrange(1, n)
        g, r, q = 1, 1, 1
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = (q * abs(x - y)) % n
                g = math.gcd(q, n)
                k += m
            r *= 2
        if g == n:
            while True:
                ys = (ys * ys + c) % n
                g = math.gcd(abs(x - ys), n)
                if g > 1:
                    break
        if g != n:
            return g
    return None


def benchmark() -> None:
    targets = [8051, 100000007 * 100000037, 1000003 * 999983]
    print(f"{'fn':<18}{'n':>25}{'factor':>14}{'ms':>10}")
    for fn in (trial_division, pollard_floyd, pollard_brent):
        for n in targets:
            if fn is trial_division and n > 10**10:
                continue
            t = time.perf_counter()
            f = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{n:>25}{str(f):>14}{dt:>10.3f}")


if __name__ == "__main__":
    benchmark()
