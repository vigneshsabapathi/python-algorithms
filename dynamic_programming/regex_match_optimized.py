#!/usr/bin/env python3
"""
Optimized and alternative implementations of Regex Match DP.

Variants covered:
1. regex_match_recursive   -- top-down memoized recursion
2. regex_match_space_opt   -- O(n) space with two rows
3. regex_match_nfa         -- NFA simulation approach

Run:
    python dynamic_programming/regex_match_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.regex_match import regex_match as reference


# ---------------------------------------------------------------------------
# Variant 1 — Top-down memoized recursion
# ---------------------------------------------------------------------------

def regex_match_recursive(text: str, pattern: str) -> bool:
    """
    Regex match using top-down memoization.

    >>> regex_match_recursive("aa", "a")
    False
    >>> regex_match_recursive("aa", "a*")
    True
    >>> regex_match_recursive("ab", ".*")
    True
    >>> regex_match_recursive("aab", "c*a*b")
    True
    >>> regex_match_recursive("", "")
    True
    """
    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> bool:
        if j == len(pattern):
            return i == len(text)
        first_match = i < len(text) and (pattern[j] == text[i] or pattern[j] == ".")
        if j + 1 < len(pattern) and pattern[j + 1] == "*":
            return dp(i, j + 2) or (first_match and dp(i + 1, j))
        return first_match and dp(i + 1, j + 1)

    result = dp(0, 0)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Variant 2 — Space-optimized (two rows)
# ---------------------------------------------------------------------------

def regex_match_space_opt(text: str, pattern: str) -> bool:
    """
    Regex match with O(n) space.

    >>> regex_match_space_opt("aa", "a")
    False
    >>> regex_match_space_opt("aa", "a*")
    True
    >>> regex_match_space_opt("ab", ".*")
    True
    >>> regex_match_space_opt("aab", "c*a*b")
    True
    >>> regex_match_space_opt("", "")
    True
    """
    m, n = len(text), len(pattern)
    prev = [False] * (n + 1)
    prev[0] = True
    for j in range(2, n + 1):
        if pattern[j - 1] == "*":
            prev[j] = prev[j - 2]

    for i in range(1, m + 1):
        curr = [False] * (n + 1)
        for j in range(1, n + 1):
            if pattern[j - 1] == "*":
                curr[j] = curr[j - 2]
                if pattern[j - 2] == "." or pattern[j - 2] == text[i - 1]:
                    curr[j] = curr[j] or prev[j]
            elif pattern[j - 1] == "." or pattern[j - 1] == text[i - 1]:
                curr[j] = prev[j - 1]
        prev = curr

    return prev[n]


# ---------------------------------------------------------------------------
# Variant 3 — NFA simulation
# ---------------------------------------------------------------------------

def regex_match_nfa(text: str, pattern: str) -> bool:
    """
    Regex match using NFA (Non-deterministic Finite Automaton) simulation.

    >>> regex_match_nfa("aa", "a")
    False
    >>> regex_match_nfa("aa", "a*")
    True
    >>> regex_match_nfa("ab", ".*")
    True
    >>> regex_match_nfa("aab", "c*a*b")
    True
    >>> regex_match_nfa("", "")
    True
    """
    # Build NFA states from pattern
    n = len(pattern)
    # States that can be reached without consuming input (epsilon transitions)
    def add_epsilon(states: set[int]) -> set[int]:
        result = set(states)
        changed = True
        while changed:
            changed = False
            new = set()
            for s in result:
                if s + 1 < n and pattern[s + 1] == "*":
                    if s + 2 not in result:
                        new.add(s + 2)
            if new - result:
                result |= new
                changed = True
        return result

    current_states = add_epsilon({0})

    for ch in text:
        next_states = set()
        for s in current_states:
            if s < n and (pattern[s] == ch or pattern[s] == "."):
                # Check if next is *, if so we advance by 2 or stay
                if s + 1 < n and pattern[s + 1] == "*":
                    next_states.add(s)  # stay (more matches)
                    next_states.add(s + 2)  # done matching
                else:
                    next_states.add(s + 1)
        current_states = add_epsilon(next_states)

    return n in current_states


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("aa", "a", False),
    ("aa", "a*", True),
    ("ab", ".*", True),
    ("aab", "c*a*b", True),
    ("mississippi", "mis*is*p*.", False),
    ("", "", True),
    ("", "a*", True),
]

IMPLS = [
    ("reference", reference),
    ("recursive", regex_match_recursive),
    ("space_opt", regex_match_space_opt),
    ("nfa", regex_match_nfa),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for text, pattern, expected in TEST_CASES:
        results = {name: fn(text, pattern) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] ({text!r}, {pattern!r})  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 20_000
    t_text, t_pat = "aaaaab", "a*a*a*a*a*b"
    print(f"\n=== Benchmark: {REPS} runs, ({t_text!r}, {t_pat!r}) ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(t_text, t_pat), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
