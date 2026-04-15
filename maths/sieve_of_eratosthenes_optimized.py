"""
Sieve of Eratosthenes — advanced variants + benchmark.

1. list_bool         - reference implementation with list[bool]
2. bytearray_slice   - bytearray + slice assignment (fast pure-python)
3. odd_only          - store only odd indices, halving memory
4. linear_sieve      - Euler's linear sieve (O(n), but more overhead)
"""
from __future__ import annotations

import math
import time


def list_bool(n: int) -> list[int]:
    if n < 2:
        return []
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i, v in enumerate(is_p) if v]


def bytearray_slice(n: int) -> list[int]:
    if n < 2:
        return []
    s = bytearray([1]) * (n + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(n)) + 1):
        if s[i]:
            s[i * i :: i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i in range(n + 1) if s[i]]


def odd_only(n: int) -> list[int]:
    if n < 2:
        return []
    if n == 2:
        return [2]
    size = (n - 1) // 2
    s = bytearray([1]) * (size + 1)
    for i in range(1, (int(math.isqrt(n)) - 1) // 2 + 1):
        if s[i]:
            p = 2 * i + 1
            start = (p * p - 3) // 2
            s[start :: p] = b"\x00" * (((size - start) // p) + 1)
    out = [2]
    out.extend(2 * i + 3 for i, v in enumerate(s) if v)
    return [p for p in out if p <= n]


def linear_sieve(n: int) -> list[int]:
    if n < 2:
        return []
    spf = [0] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > n:
                break
            spf[i * p] = p
    return primes


def benchmark() -> None:
    print(f"{'fn':<20}{'n':>10}{'count':>10}{'ms':>12}")
    for n in (10**5, 10**6, 5 * 10**6):
        for fn in (list_bool, bytearray_slice, odd_only, linear_sieve):
            t = time.perf_counter()
            p = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<20}{n:>10}{len(p):>10}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
