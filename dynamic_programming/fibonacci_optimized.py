#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fibonacci Sequence.

Four variants:
  class_based   — Fibonacci class with cached list (reference)
  generator     — Python generator yielding F(0), F(1), ...
  dict_memo     — dictionary-based memoization
  tuple_rolling — tuple unpacking O(1) space

Run:
    python dynamic_programming/fibonacci_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.fibonacci import Fibonacci

_fib_ref = Fibonacci()


def reference(n: int) -> list[int]:
    return Fibonacci().get(n)


# ---------------------------------------------------------------------------
# Variant 1 — class_based (same as reference)
# ---------------------------------------------------------------------------

def class_based(n: int) -> list[int]:
    """
    >>> class_based(10)
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    return reference(n)


# ---------------------------------------------------------------------------
# Variant 2 — generator: Python generator
# ---------------------------------------------------------------------------

def generator(n: int) -> list[int]:
    """
    >>> generator(10)
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    def fib_gen():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    result = []
    gen = fib_gen()
    for _ in range(n):
        result.append(next(gen))
    return result


# ---------------------------------------------------------------------------
# Variant 3 — dict_memo: Dictionary memoization
# ---------------------------------------------------------------------------

def dict_memo(n: int) -> list[int]:
    """
    >>> dict_memo(10)
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    cache: dict[int, int] = {0: 0, 1: 1}

    def fib(k: int) -> int:
        if k not in cache:
            cache[k] = fib(k - 1) + fib(k - 2)
        return cache[k]

    return [fib(i) for i in range(n)]


# ---------------------------------------------------------------------------
# Variant 4 — tuple_rolling: O(1) space rolling
# ---------------------------------------------------------------------------

def tuple_rolling(n: int) -> list[int]:
    """
    >>> tuple_rolling(10)
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    """
    if n <= 0:
        return []
    result = [0]
    if n == 1:
        return result
    a, b = 0, 1
    for _ in range(n - 1):
        result.append(b)
        a, b = b, a + b
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("class_based", class_based),
    ("generator", generator),
    ("dict_memo", dict_memo),
    ("tuple_rolling", tuple_rolling),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for n in [1, 5, 10, 20]:
        ref = reference(n)
        for name, fn in IMPLS:
            result = fn(n)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({n}) = {result[:5]}...")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 50_000
    print(f"\n=== Benchmark (n=20): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(20), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
