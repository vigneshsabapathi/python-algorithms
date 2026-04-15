"""
Twin primes — variants + benchmark.

1. trial_filter     - filter primes-up-to-n list for p+2 also prime
2. sieve_then_scan  - sieve once, scan adjacent primes
3. miller_rabin     - test individually with deterministic Miller-Rabin
"""
from __future__ import annotations

import math
import time


def _sieve(n: int) -> list[bool]:
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(n)) + 1):
        if s[i]:
            s[i * i :: i] = b"\x00" * (((n - i * i) // i) + 1)
    return list(s)


def trial_filter(n: int):
    s = _sieve(n)
    return [(p, p + 2) for p in range(3, n - 1) if s[p] and s[p + 2]]


def sieve_then_scan(n: int):
    s = _sieve(n)
    primes = [i for i, v in enumerate(s) if v]
    return [(primes[i], primes[i + 1]) for i in range(len(primes) - 1) if primes[i + 1] - primes[i] == 2]


def _mr(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
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


def miller_rabin(n: int):
    return [(p, p + 2) for p in range(3, n - 1, 2) if _mr(p) and _mr(p + 2)]


def benchmark() -> None:
    print(f"{'fn':<18}{'n':>10}{'count':>8}{'ms':>12}")
    for n in (10_000, 100_000, 1_000_000):
        for fn in (trial_filter, sieve_then_scan, miller_rabin):
            if fn is miller_rabin and n > 100_000:
                continue
            t = time.perf_counter()
            r = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{n:>10}{len(r):>8}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
