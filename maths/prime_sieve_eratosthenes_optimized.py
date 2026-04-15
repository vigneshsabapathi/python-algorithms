"""
Eratosthenes sieve — optimized variants + benchmark.

1. basic_list         - list-of-bool reference
2. bytearray_slice    - bytearray with slice-assignment for speed
3. odd_only           - represent only odd numbers, halving memory
4. numpy_sieve        - vectorized numpy marking
"""
from __future__ import annotations

import math
import time


def basic_list(n: int) -> list[int]:
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
    is_p = bytearray([1]) * (n + 1)
    is_p[0] = is_p[1] = 0
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_p[i]:
            is_p[i * i :: i] = b"\x00" * (((n - i * i) // i) + 1)
    return [i for i in range(n + 1) if is_p[i]]


def odd_only(n: int) -> list[int]:
    if n < 2:
        return []
    if n == 2:
        return [2]
    size = (n - 1) // 2  # represents 3,5,7,9,...
    sieve = bytearray([1]) * (size + 1)
    for i in range(1, (int(math.isqrt(n)) - 1) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p - 3) // 2
            sieve[start :: p] = b"\x00" * (((size - start) // p) + 1)
    out = [2]
    out.extend(2 * i + 3 for i, v in enumerate(sieve) if v)
    return [p for p in out if p <= n]


def numpy_sieve(n: int) -> list[int]:
    try:
        import numpy as np
    except ImportError:
        return basic_list(n)
    if n < 2:
        return []
    is_p = np.ones(n + 1, dtype=bool)
    is_p[:2] = False
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_p[i]:
            is_p[i * i :: i] = False
    return np.flatnonzero(is_p).tolist()


def benchmark() -> None:
    print(f"{'fn':<20}{'n':>12}{'count':>10}{'ms':>12}")
    for n in (10_000, 100_000, 1_000_000, 5_000_000):
        for fn in (basic_list, bytearray_slice, odd_only, numpy_sieve):
            t = time.perf_counter()
            p = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<20}{n:>12}{len(p):>10}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
