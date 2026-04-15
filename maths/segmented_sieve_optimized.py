"""
Segmented sieve variants + benchmark.

1. basic_segmented   - straight implementation
2. windowed          - process [lo, hi] in fixed-size windows
3. full_sieve_ref    - allocate full sieve up to hi (for comparison)
"""
from __future__ import annotations

import math
import time


def _base_primes(r: int) -> list[int]:
    s = bytearray([1]) * (r + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(r)) + 1):
        if s[i]:
            s[i * i :: i] = b"\x00" * (((r - i * i) // i) + 1)
    return [i for i in range(r + 1) if s[i]]


def basic_segmented(lo: int, hi: int) -> list[int]:
    if hi < 2:
        return []
    lo = max(lo, 2)
    primes = _base_primes(int(math.isqrt(hi)))
    mark = bytearray([1]) * (hi - lo + 1)
    for p in primes:
        start = max(p * p, ((lo + p - 1) // p) * p)
        mark[start - lo :: p] = b"\x00" * (((hi - start) // p) + 1)
    return [lo + i for i in range(len(mark)) if mark[i]]


def windowed(lo: int, hi: int, window: int = 1 << 16) -> list[int]:
    if hi < 2:
        return []
    lo = max(lo, 2)
    primes = _base_primes(int(math.isqrt(hi)))
    out: list[int] = []
    cur = lo
    while cur <= hi:
        end = min(cur + window - 1, hi)
        mark = bytearray([1]) * (end - cur + 1)
        for p in primes:
            start = max(p * p, ((cur + p - 1) // p) * p)
            if start > end:
                continue
            mark[start - cur :: p] = b"\x00" * (((end - start) // p) + 1)
        out.extend(cur + i for i in range(len(mark)) if mark[i])
        cur = end + 1
    return out


def full_sieve_ref(lo: int, hi: int) -> list[int]:
    if hi < 2:
        return []
    s = bytearray([1]) * (hi + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(hi)) + 1):
        if s[i]:
            s[i * i :: i] = b"\x00" * (((hi - i * i) // i) + 1)
    return [i for i in range(max(lo, 2), hi + 1) if s[i]]


def benchmark() -> None:
    ranges = [(10**6, 10**6 + 10_000), (10**9, 10**9 + 10_000)]
    print(f"{'fn':<18}{'range':>28}{'count':>8}{'ms':>12}")
    for fn in (basic_segmented, windowed, full_sieve_ref):
        for lo, hi in ranges:
            if fn is full_sieve_ref and hi > 10**8:
                continue
            t = time.perf_counter()
            p = fn(lo, hi)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{f'[{lo},{hi}]':>28}{len(p):>8}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
