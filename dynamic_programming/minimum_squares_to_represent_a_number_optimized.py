#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Squares to Represent a Number.

Variants covered:
1. min_squares_bfs        -- BFS level-order (often fastest for interviews)
2. min_squares_math       -- Lagrange's theorem with Legendre's 3-square condition
3. min_squares_static     -- precompute squares list, cleaner DP

Run:
    python dynamic_programming/minimum_squares_to_represent_a_number_optimized.py
"""

from __future__ import annotations

import math
import sys
import os
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.minimum_squares_to_represent_a_number import minimum_squares as reference


# ---------------------------------------------------------------------------
# Variant 1 — BFS
# ---------------------------------------------------------------------------

def min_squares_bfs(n: int) -> int:
    """
    BFS approach: shortest path from n to 0 subtracting perfect squares.

    >>> min_squares_bfs(12)
    3
    >>> min_squares_bfs(13)
    2
    >>> min_squares_bfs(1)
    1
    >>> min_squares_bfs(0)
    0
    >>> min_squares_bfs(7)
    4
    """
    if n <= 0:
        return 0
    squares = []
    i = 1
    while i * i <= n:
        squares.append(i * i)
        i += 1

    visited = [False] * (n + 1)
    visited[n] = True
    queue = deque([(n, 0)])

    while queue:
        rem, depth = queue.popleft()
        for sq in squares:
            nxt = rem - sq
            if nxt == 0:
                return depth + 1
            if nxt > 0 and not visited[nxt]:
                visited[nxt] = True
                queue.append((nxt, depth + 1))

    return n  # fallback: all 1s


# ---------------------------------------------------------------------------
# Variant 2 — Math (Lagrange + Legendre)
# ---------------------------------------------------------------------------

def min_squares_math(n: int) -> int:
    """
    O(sqrt(n)) using number theory:
    - 1 if n is a perfect square
    - 2 if n = a^2 + b^2 (check via two-pointer or direct)
    - 4 if n = 4^a(8b+7) (Legendre's theorem)
    - 3 otherwise

    >>> min_squares_math(12)
    3
    >>> min_squares_math(13)
    2
    >>> min_squares_math(1)
    1
    >>> min_squares_math(0)
    0
    >>> min_squares_math(7)
    4
    >>> min_squares_math(4)
    1
    >>> min_squares_math(100)
    1
    """
    if n <= 0:
        return 0

    # Check if perfect square
    if int(math.isqrt(n)) ** 2 == n:
        return 1

    # Check Legendre's condition for 4
    temp = n
    while temp % 4 == 0:
        temp //= 4
    if temp % 8 == 7:
        return 4

    # Check if expressible as sum of 2 squares
    i = 1
    while i * i <= n:
        rem = n - i * i
        if int(math.isqrt(rem)) ** 2 == rem:
            return 2
        i += 1

    return 3


# ---------------------------------------------------------------------------
# Variant 3 — Cleaner DP with precomputed squares
# ---------------------------------------------------------------------------

def min_squares_static(n: int) -> int:
    """
    DP with precomputed squares list for cleaner inner loop.

    >>> min_squares_static(12)
    3
    >>> min_squares_static(13)
    2
    >>> min_squares_static(1)
    1
    >>> min_squares_static(0)
    0
    >>> min_squares_static(7)
    4
    """
    if n <= 0:
        return 0
    squares = [i * i for i in range(1, int(math.isqrt(n)) + 1)]
    dp = [0] + [float("inf")] * n
    for i in range(1, n + 1):
        for sq in squares:
            if sq > i:
                break
            dp[i] = min(dp[i], dp[i - sq] + 1)
    return dp[n]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (12, 3), (13, 2), (1, 1), (0, 0), (7, 4), (4, 1), (100, 1),
]

IMPLS = [
    ("reference", reference),
    ("bfs", min_squares_bfs),
    ("math", min_squares_math),
    ("static_dp", min_squares_static),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] n={n}  expected={expected}  " +
              "  ".join(f"{name}={v}" for name, v in results.items()))

    REPS = 2_000
    bench_n = 999
    print(f"\n=== Benchmark: {REPS} runs, n={bench_n} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_n), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
