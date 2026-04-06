#!/usr/bin/env python3
"""
Optimized and alternative implementations of Generate Parentheses.

Variants covered:
1. generate_iterative      -- BFS/queue-based iterative generation (no recursion).
2. generate_generator      -- generator version; yields one string at a time.
3. generate_dp             -- DP via Catalan recurrence:
                              C(n) = C(0)*C(n-1) + C(1)*C(n-2) + ... + C(n-1)*C(0)
                              Builds n-pair results from smaller solutions.
4. count_only              -- math.comb Catalan number; O(n), no generation.

Key interview insight:
    The count of valid parenthesizations for n pairs = Catalan number C_n.
    C_n = C(2n,n)/(n+1).  C_0=1, C_1=1, C_2=2, C_3=5, C_4=14, C_5=42.
    The backtracking approach generates exactly C_n strings — it never
    generates invalid strings (pruning is perfect: only valid prefixes explored).

Run:
    python backtracking/generate_parentheses_optimized.py
"""

from __future__ import annotations

import sys
import os
import math
import timeit
from collections import deque
from typing import Generator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.generate_parentheses import generate_parenthesis


# ---------------------------------------------------------------------------
# Variant 1 — iterative BFS
# ---------------------------------------------------------------------------


def generate_iterative(n: int) -> list[str]:
    """
    BFS/queue-based generation of valid parentheses.
    Each queue entry: (partial_string, open_count, close_count).

    No recursion — avoids Python stack depth limit for large n.

    >>> generate_iterative(2)
    ['(())', '()()']
    >>> generate_iterative(1)
    ['()']
    >>> generate_iterative(0)
    ['']
    >>> generate_iterative(3)
    ['((()))', '(()())', '(())()', '()(())', '()()()']
    """
    if n == 0:
        return [""]
    result: list[str] = []
    queue: deque[tuple[str, int, int]] = deque([("", 0, 0)])
    while queue:
        partial, opened, closed = queue.popleft()
        if len(partial) == 2 * n:
            result.append(partial)
            continue
        if opened < n:
            queue.append((partial + "(", opened + 1, closed))
        if closed < opened:
            queue.append((partial + ")", opened, closed + 1))
    return result


# ---------------------------------------------------------------------------
# Variant 2 — generator (lazy, memory-efficient)
# ---------------------------------------------------------------------------


def generate_generator(n: int) -> Generator[str, None, None]:
    """
    Generator-based backtracking: yields one valid string at a time.
    O(n) memory instead of O(C_n * 2n) to store all results.
    Useful for early exit (e.g., find the first valid combination).

    >>> list(generate_generator(2))
    ['(())', '()()']
    >>> list(generate_generator(1))
    ['()']
    >>> list(generate_generator(0))
    ['']
    """

    def _bt(partial: str, opened: int, closed: int) -> Generator[str, None, None]:
        if len(partial) == 2 * n:
            yield partial
            return
        if opened < n:
            yield from _bt(partial + "(", opened + 1, closed)
        if closed < opened:
            yield from _bt(partial + ")", opened, closed + 1)

    yield from _bt("", 0, 0)


# ---------------------------------------------------------------------------
# Variant 3 — DP via Catalan recurrence
# ---------------------------------------------------------------------------


def generate_dp(n: int) -> list[str]:
    """
    Build valid parentheses via the Catalan recurrence:
        C(n) = { '(' + p + ')' + q  for k in 0..n-1
                  for p in C(k), for q in C(n-1-k) }

    This directly mirrors the mathematical structure: the first '(' and its
    matching ')' wrap exactly k inner pairs; the remaining n-1-k pairs follow.

    >>> sorted(generate_dp(2))
    ['(())', '()()']
    >>> generate_dp(1)
    ['()']
    >>> generate_dp(0)
    ['']
    >>> sorted(generate_dp(3)) == sorted(generate_parenthesis(3))
    True
    """
    dp: list[list[str]] = [[] for _ in range(n + 1)]
    dp[0] = [""]
    for i in range(1, n + 1):
        for k in range(i):
            for inner in dp[k]:
                for outer in dp[i - 1 - k]:
                    dp[i].append(f"({inner}){outer}")
    return dp[n]


# ---------------------------------------------------------------------------
# Variant 4 — count only (Catalan number)
# ---------------------------------------------------------------------------


def catalan(n: int) -> int:
    """
    Return the n-th Catalan number = C(2n, n) / (n+1).
    This equals the number of valid parenthesizations for n pairs.

    O(n) time, O(1) space.

    >>> catalan(0)
    1
    >>> catalan(1)
    1
    >>> catalan(2)
    2
    >>> catalan(3)
    5
    >>> catalan(4)
    14
    >>> catalan(5)
    42
    >>> catalan(10)
    16796
    """
    return math.comb(2 * n, n) // (n + 1)


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:
    print("\n=== Correctness: counts match Catalan numbers ===")
    for n in range(7):
        ref = generate_parenthesis(n)
        ite = generate_iterative(n)
        gen = list(generate_generator(n))
        dp = generate_dp(n)
        cat = catalan(n)
        all_match = (
            sorted(ref) == sorted(ite) == sorted(gen) == sorted(dp)
            and len(ref) == cat
        )
        print(f"  n={n}  C_{n}={cat:>4}  {'OK' if all_match else 'MISMATCH'}")

    REPS = 3000
    print(f"\n=== Benchmark ({REPS} runs each) ===")
    print(f"  {'n':>3} {'C_n':>6}  {'backtrack':>12}  {'iterative':>12}  "
          f"{'generator':>12}  {'dp':>10}")

    for n in [4, 6, 8, 10]:
        cn = catalan(n)
        t1 = timeit.timeit(lambda: generate_parenthesis(n), number=REPS) * 1000 / REPS
        t2 = timeit.timeit(lambda: generate_iterative(n), number=REPS) * 1000 / REPS
        t3 = timeit.timeit(lambda: list(generate_generator(n)), number=REPS) * 1000 / REPS
        t4 = timeit.timeit(lambda: generate_dp(n), number=REPS) * 1000 / REPS
        print(f"  {n:>3} {cn:>6}  {t1:>11.4f}ms  {t2:>11.4f}ms  "
              f"{t3:>11.4f}ms  {t4:>9.4f}ms")

    print("\n=== Catalan numbers (count only) ===")
    for n in [5, 10, 15, 20]:
        t = timeit.timeit(lambda: catalan(n), number=100000) * 1000 / 100000
        print(f"  C_{n:<2} = {catalan(n):>10}  {t:.6f} ms/call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
