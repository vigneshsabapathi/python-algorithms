"""
Prime factorization variants + benchmark.

1. trial_division   - standard O(sqrt n)
2. wheel_2_3_5      - skip multiples of 2/3/5 via wheel pattern
3. with_pollard     - combine small primes + Pollard's rho for big factors
"""
from __future__ import annotations

import math
import random
import time


def trial_division(n: int) -> list[int]:
    out = []
    while n % 2 == 0:
        out.append(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            out.append(i)
            n //= i
        i += 2
    if n > 1:
        out.append(n)
    return out


def wheel_2_3_5(n: int) -> list[int]:
    out = []
    for p in (2, 3, 5):
        while n % p == 0:
            out.append(p)
            n //= p
    increments = (4, 2, 4, 2, 4, 6, 2, 6)
    i = 7
    idx = 0
    while i * i <= n:
        while n % i == 0:
            out.append(i)
            n //= i
        i += increments[idx]
        idx = (idx + 1) % len(increments)
    if n > 1:
        out.append(n)
    return out


def _is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        x = random.randrange(2, n)
        y = x
        c = random.randrange(1, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def with_pollard(n: int) -> list[int]:
    out = []
    # trial-divide by small primes
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
        while n % p == 0:
            out.append(p)
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if _is_probable_prime(m):
            out.append(m)
            continue
        d = _rho(m)
        stack.append(d)
        stack.append(m // d)
    return sorted(out)


def benchmark() -> None:
    targets = [360, 999983, 1000003 * 999983, 2**20 * 3**4]
    funcs = [trial_division, wheel_2_3_5, with_pollard]
    print(f"{'fn':<16}{'n':>22}{'factors':>30}{'ms':>10}")
    for fn in funcs:
        for n in targets:
            t = time.perf_counter()
            f = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<16}{n:>22}{str(f)[:30]:>30}{dt:>10.3f}")


if __name__ == "__main__":
    benchmark()
