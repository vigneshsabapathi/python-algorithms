"""
Multiplication table variants + benchmark.

1. list_comp      - list comprehension with f-strings
2. generator      - lazy generator (doesn't pre-build)
3. str_join       - single str.join build
4. grid_2d        - produce whole 2D grid 1..n × 1..n
"""
from __future__ import annotations

import time
from typing import Iterator, List


def list_comp(n: int, size: int = 10) -> List[str]:
    return [f"{n} x {i} = {n * i}" for i in range(1, size + 1)]


def generator(n: int, size: int = 10) -> Iterator[str]:
    for i in range(1, size + 1):
        yield f"{n} x {i} = {n * i}"


def str_join(n: int, size: int = 10) -> str:
    return "\n".join(f"{n} x {i} = {n * i}" for i in range(1, size + 1))


def grid_2d(n: int) -> List[List[int]]:
    return [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]


def benchmark() -> None:
    print(f"{'fn':<14}{'size':>8}{'ms':>12}")
    for size in (10, 100, 1000):
        for fn in (list_comp, lambda n, s=size: list(generator(n, s)), str_join):
            t = time.perf_counter()
            for _ in range(1000):
                fn(7, size)
            dt = (time.perf_counter() - t) * 1000
            name = fn.__name__ if hasattr(fn, "__name__") and fn.__name__ != "<lambda>" else "generator"
            print(f"{name:<14}{size:>8}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
