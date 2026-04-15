"""
Sum-of-digits variants + benchmark.

1. arithmetic    - repeated divmod (fastest for ints)
2. str_based     - sum(int(c) for c in str(n))
3. recursive     - recursive digit extraction
4. map_ord       - sum(ord(c) - 48 for c in str(n))
"""
from __future__ import annotations

import time


def arithmetic(n: int) -> int:
    n = abs(n)
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


def str_based(n: int) -> int:
    return sum(int(c) for c in str(abs(n)))


def recursive(n: int) -> int:
    n = abs(n)
    return 0 if n == 0 else (n % 10) + recursive(n // 10)


def map_ord(n: int) -> int:
    return sum(ord(c) - 48 for c in str(abs(n)))


def benchmark() -> None:
    nums = [10**6, 10**18, 10**100]
    print(f"{'fn':<14}{'digits':>8}{'ms':>12}")
    for fn in (arithmetic, str_based, map_ord):
        for n in nums:
            t = time.perf_counter()
            for _ in range(10000):
                fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<14}{len(str(n)):>8}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
