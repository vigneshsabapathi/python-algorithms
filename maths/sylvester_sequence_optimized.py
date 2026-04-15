"""
Sylvester's sequence — variants + benchmark.

1. iterative   - straight loop, accumulating ints
2. recursive   - direct recursion
3. generator   - lazy generator (memory-efficient)
"""
from __future__ import annotations

import sys
import time
from typing import Iterator


def iterative(n: int) -> list[int]:
    out, cur = [], 2
    for _ in range(n):
        out.append(cur)
        cur = cur * cur - cur + 1
    return out


def recursive(n: int) -> list[int]:
    sys.setrecursionlimit(max(2000, n + 50))

    def _term(k: int) -> int:
        if k == 0:
            return 2
        a = _term(k - 1)
        return a * a - a + 1

    return [_term(k) for k in range(n)]


def gen() -> Iterator[int]:
    cur = 2
    while True:
        yield cur
        cur = cur * cur - cur + 1


def benchmark() -> None:
    print(f"{'fn':<14}{'n':>6}{'ms':>12}")
    for n in (5, 8, 10):
        for name, fn in [("iterative", iterative), ("generator", lambda n=n: [next(gen()) for _ in range(n)])]:
            t = time.perf_counter()
            fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{name:<14}{n:>6}{dt:>12.4f}")


if __name__ == "__main__":
    benchmark()
