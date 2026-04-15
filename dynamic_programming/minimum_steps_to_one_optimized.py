#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Steps to One.

Variants covered:
1. min_steps_bfs          -- BFS shortest path
2. min_steps_greedy_memo  -- greedy-first with memoization
3. min_steps_with_path    -- DP that also reconstructs the path

Run:
    python dynamic_programming/minimum_steps_to_one_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from collections import deque
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.minimum_steps_to_one import minimum_steps_to_one as reference


# ---------------------------------------------------------------------------
# Variant 1 — BFS
# ---------------------------------------------------------------------------

def min_steps_bfs(n: int) -> int:
    """
    BFS from n to 1 — each level is one step.

    >>> min_steps_bfs(1)
    0
    >>> min_steps_bfs(10)
    3
    >>> min_steps_bfs(15)
    4
    >>> min_steps_bfs(6)
    2
    """
    if n <= 1:
        return 0
    visited = set()
    queue = deque([(n, 0)])
    visited.add(n)
    while queue:
        val, steps = queue.popleft()
        for nxt in [val - 1] + ([val // 2] if val % 2 == 0 else []) + ([val // 3] if val % 3 == 0 else []):
            if nxt == 1:
                return steps + 1
            if nxt > 1 and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, steps + 1))
    return -1


# ---------------------------------------------------------------------------
# Variant 2 — Top-down memoization
# ---------------------------------------------------------------------------

def min_steps_greedy_memo(n: int) -> int:
    """
    Top-down with memoization.

    >>> min_steps_greedy_memo(1)
    0
    >>> min_steps_greedy_memo(10)
    3
    >>> min_steps_greedy_memo(15)
    4
    >>> min_steps_greedy_memo(6)
    2
    """
    @lru_cache(maxsize=None)
    def dp(x: int) -> int:
        if x <= 1:
            return 0
        best = dp(x - 1) + 1
        if x % 2 == 0:
            best = min(best, dp(x // 2) + 1)
        if x % 3 == 0:
            best = min(best, dp(x // 3) + 1)
        return best

    result = dp(n)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Variant 3 — DP with path reconstruction
# ---------------------------------------------------------------------------

def min_steps_with_path(n: int) -> tuple[int, list[int]]:
    """
    Returns (min_steps, path_from_n_to_1).

    >>> min_steps_with_path(1)
    (0, [1])
    >>> min_steps_with_path(10)
    (3, [10, 9, 3, 1])
    >>> min_steps_with_path(6)
    (2, [6, 3, 1])
    """
    if n <= 1:
        return (0, [1])

    dp = [0] * (n + 1)
    parent = [0] * (n + 1)

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + 1
        parent[i] = i - 1
        if i % 2 == 0 and dp[i // 2] + 1 < dp[i]:
            dp[i] = dp[i // 2] + 1
            parent[i] = i // 2
        if i % 3 == 0 and dp[i // 3] + 1 < dp[i]:
            dp[i] = dp[i // 3] + 1
            parent[i] = i // 3

    path = []
    cur = n
    while cur >= 1:
        path.append(cur)
        if cur == 1:
            break
        cur = parent[cur]

    return (dp[n], path)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (1, 0), (10, 3), (15, 4), (6, 2), (2, 1), (4, 2),
]

IMPLS = [
    ("reference", reference),
    ("bfs", min_steps_bfs),
    ("memo", min_steps_greedy_memo),
    ("with_path", lambda n: min_steps_with_path(n)[0]),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] n={n}  expected={expected}  " +
              "  ".join(f"{name}={v}" for name, v in results.items()))

    # Show path for n=10
    steps, path = min_steps_with_path(10)
    print(f"\n  Path for n=10: {' -> '.join(map(str, path))} ({steps} steps)")

    REPS = 5_000
    bench_n = 500
    print(f"\n=== Benchmark: {REPS} runs, n={bench_n} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_n), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
