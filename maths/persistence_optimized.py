"""
Multiplicative persistence variants + benchmark.

1. str_product       - convert to str, multiply char digits
2. arithmetic        - repeated modulo / divide
3. reduce_map        - functools.reduce over map

Also additive persistence for completeness.
"""
from __future__ import annotations

import time
from functools import reduce


def str_product(num: int) -> int:
    steps = 0
    while num >= 10:
        p = 1
        for c in str(num):
            p *= int(c)
        num = p
        steps += 1
    return steps


def arithmetic(num: int) -> int:
    steps = 0
    while num >= 10:
        p = 1
        x = num
        while x:
            p *= x % 10
            x //= 10
        num = p
        steps += 1
    return steps


def reduce_map(num: int) -> int:
    steps = 0
    while num >= 10:
        num = reduce(lambda a, b: a * b, (int(c) for c in str(num)), 1)
        steps += 1
    return steps


def additive_persistence(num: int) -> int:
    steps = 0
    while num >= 10:
        num = sum(int(c) for c in str(num))
        steps += 1
    return steps


def benchmark() -> None:
    xs = [39, 999, 277777788888899, 86722]
    funcs = [str_product, arithmetic, reduce_map]
    print(f"{'fn':<18}{'n':>22}{'steps':>8}{'ms':>12}")
    for fn in funcs:
        for n in xs:
            t = time.perf_counter()
            r = fn(n)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<18}{n:>22}{r:>8}{dt:>12.4f}")


if __name__ == "__main__":
    benchmark()
