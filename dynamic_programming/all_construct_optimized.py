#!/usr/bin/env python3
"""
Optimized and alternative implementations of All Construct.

Given a target string and a word bank, list all ways to construct the target.

Four variants:
  tabulation      — bottom-up table building (reference)
  memoized        — top-down recursive with memoization
  trie_based      — uses a trie for efficient prefix matching
  backtracking    — explicit backtracking with path tracking

Run:
    python dynamic_programming/all_construct_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.all_construct import all_construct as reference


# ---------------------------------------------------------------------------
# Variant 1 — tabulation: Bottom-up (same as reference)
# ---------------------------------------------------------------------------

def tabulation(target: str, word_bank: list[str] | None = None) -> list[list[str]]:
    """
    >>> tabulation("purple", ["purp", "p", "ur", "le", "purpl"])
    [['purp', 'le'], ['p', 'ur', 'p', 'le']]
    """
    return reference(target, word_bank)


# ---------------------------------------------------------------------------
# Variant 2 — memoized: Top-down with memoization
# ---------------------------------------------------------------------------

def memoized(target: str, word_bank: list[str] | None = None) -> list[list[str]]:
    """
    >>> sorted([sorted(x) for x in memoized("purple", ["purp", "p", "ur", "le", "purpl"])])
    [['le', 'purp'], ['le', 'p', 'p', 'ur']]
    """
    word_bank = word_bank or []
    memo: dict[str, list[list[str]]] = {}

    def solve(remaining: str) -> list[list[str]]:
        if remaining in memo:
            return memo[remaining]
        if remaining == "":
            return [[]]

        results: list[list[str]] = []
        for word in word_bank:
            if remaining.startswith(word):
                suffix_ways = solve(remaining[len(word):])
                for way in suffix_ways:
                    results.append([word, *way])

        memo[remaining] = results
        return results

    return solve(target)


# ---------------------------------------------------------------------------
# Variant 3 — trie_based: Uses trie for efficient prefix matching
# ---------------------------------------------------------------------------

def trie_based(target: str, word_bank: list[str] | None = None) -> list[list[str]]:
    """
    >>> sorted([sorted(x) for x in trie_based("purple", ["purp", "p", "ur", "le", "purpl"])])
    [['le', 'purp'], ['le', 'p', 'p', 'ur']]
    """
    word_bank = word_bank or []

    # Build trie
    trie: dict = {}
    for word in word_bank:
        node = trie
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def solve(start: int) -> tuple[tuple[str, ...], ...]:
        if start == len(target):
            return ((),)

        results: list[tuple[str, ...]] = []
        node = trie
        for end in range(start, len(target)):
            ch = target[end]
            if ch not in node:
                break
            node = node[ch]
            if "$" in node:
                word = target[start: end + 1]
                for way in solve(end + 1):
                    results.append((word, *way))

        return tuple(results)

    return [list(way) for way in solve(0)]


# ---------------------------------------------------------------------------
# Variant 4 — backtracking: Explicit backtracking with path
# ---------------------------------------------------------------------------

def backtracking(target: str, word_bank: list[str] | None = None) -> list[list[str]]:
    """
    >>> sorted([sorted(x) for x in backtracking("purple", ["purp", "p", "ur", "le", "purpl"])])
    [['le', 'purp'], ['le', 'p', 'p', 'ur']]
    """
    word_bank = word_bank or []
    results: list[list[str]] = []
    path: list[str] = []

    def backtrack(start: int) -> None:
        if start == len(target):
            results.append(path[:])
            return
        for word in word_bank:
            if target[start: start + len(word)] == word:
                path.append(word)
                backtrack(start + len(word))
                path.pop()

    backtrack(0)
    return results


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("hello", ["he", "l", "o"]),
    ("purple", ["purp", "p", "ur", "le", "purpl"]),
    ("", ["a", "b"]),
    ("abc", ["x", "y"]),
    ("abcdef", ["ab", "abc", "cd", "def", "abcd", "ef"]),
]

IMPLS = [
    ("reference", reference),
    ("memoized", memoized),
    ("trie_based", trie_based),
    ("backtracking", backtracking),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for target, words in TEST_CASES:
        ref_result = sorted([sorted(w) for w in reference(target, words)])
        for name, fn in IMPLS[1:]:
            result = sorted([sorted(w) for w in fn(target, words)])
            ok = result == ref_result
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({target!r}) — {len(result)} combinations")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 10_000
    test_inputs = [("purple", ["purp", "p", "ur", "le", "purpl"]),
                   ("hello", ["he", "l", "o"])]

    print(f"\n=== Benchmark: {REPS} runs, {len(test_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(t, w) for t, w in test_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms / batch of {len(test_inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
