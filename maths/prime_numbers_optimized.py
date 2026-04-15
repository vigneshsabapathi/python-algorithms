"""
Primes up to n: approaches + benchmark.

1. trial_division   - O(n sqrt n)
2. sieve            - Sieve of Eratosthenes, O(n log log n)
3. sieve_bool_bytes - same but bytearray for cache locality
4. sundaram         - Sieve of Sundaram
"""
from __future__ import annotations

import math
import time


def trial_division(n: int) -> list[int]:
    out = []
    for k in range(2, n + 1):
        ok = True
        for i in range(2, int(math.isqrt(k)) + 1):
            if k % i == 0:
                ok = False
                break
        if ok:
            out.append(k)
    return out


def sieve(n: int) -> list[int]:
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i, v in enumerate(is_p) if v]


def sieve_bool_bytes(n: int) -> list[int]:
    if n < 2:
        return []
    is_p = bytearray([1]) * (n + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_p[i]:
            is_p[i * i :: i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i in range(n + 1) if is_p[i]]


def sundaram(n: int) -> list[int]:
    if n < 2:
        return []
    k = (n - 1) // 2
    marked = [False] * (k + 1)
    for i in range(1, k + 1):
        j = i
        while i + j + 2 * i * j <= k:
            marked[i + j + 2 * i * j] = True
            j += 1
    out = [2]
    for i in range(1, k + 1):
        if not marked[i]:
            out.append(2 * i + 1)
    return [p for p in out if p <= n]


def benchmark() -> None:
    print(f"{'fn':<22}{'n':>10}{'count':>10}{'ms':>12}")
    for n in (1_000, 10_000, 100_000, 1_000_000):
        for fn in (trial_division, sieve, sieve_bool_bytes, sundaram):
            if fn is trial_division and n > 10_000:
                continue
            t = time.perf_counter()
            p = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<22}{n:>10}{len(p):>10}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
