"""
Power computation variants + benchmark.

1. naive_recursion    - O(n) recursion
2. fast_exp_recursive - exponentiation by squaring, O(log n)
3. fast_exp_iterative - iterative log n version (no recursion)
4. builtin_pow        - Python's ** operator (uses C implementation)
"""
from __future__ import annotations

import time


def naive_recursion(b: float, e: int) -> float:
    if e == 0:
        return 1
    if e < 0:
        return 1 / naive_recursion(b, -e)
    return b * naive_recursion(b, e - 1)


def fast_exp_recursive(b: float, e: int) -> float:
    if e == 0:
        return 1
    if e < 0:
        return 1 / fast_exp_recursive(b, -e)
    h = fast_exp_recursive(b, e // 2)
    return h * h if e % 2 == 0 else h * h * b


def fast_exp_iterative(b: float, e: int) -> float:
    if e < 0:
        return 1 / fast_exp_iterative(b, -e)
    r = 1
    while e > 0:
        if e & 1:
            r *= b
        b *= b
        e >>= 1
    return r


def builtin_pow(b: float, e: int) -> float:
    return b**e


def benchmark() -> None:
    import sys

    sys.setrecursionlimit(5000)
    print(f"{'fn':<22}{'exp':>8}{'ms':>12}")
    for e in (10, 100, 1000):
        for fn in (naive_recursion, fast_exp_recursive, fast_exp_iterative, builtin_pow):
            if fn is naive_recursion and e > 900:
                continue
            t = time.perf_counter()
            for _ in range(1000):
                fn(1.0001, e)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<22}{e:>8}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
