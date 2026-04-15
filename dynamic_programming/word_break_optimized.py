#!/usr/bin/env python3
"""
Optimized and alternative implementations of Word Break.

Variants covered:
1. word_break_trie       -- Trie-based matching for efficient prefix lookup
2. word_break_bfs        -- BFS approach
3. word_break_all_segs   -- returns all valid segmentations

Run:
    python dynamic_programming/word_break_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from collections import deque
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.word_break import word_break as reference


# ---------------------------------------------------------------------------
# Variant 1 — Trie-based
# ---------------------------------------------------------------------------

def word_break_trie(s: str, word_dict: list[str]) -> bool:
    """
    Word break using a Trie for efficient prefix matching.

    >>> word_break_trie("leetcode", ["leet", "code"])
    True
    >>> word_break_trie("applepenapple", ["apple", "pen"])
    True
    >>> word_break_trie("catsandog", ["cats", "dog", "sand", "and", "cat"])
    False
    >>> word_break_trie("", ["a"])
    True
    >>> word_break_trie("aaaaaaa", ["aaaa", "aaa"])
    True
    """
    # Build trie
    trie: dict = {}
    for word in word_dict:
        node = trie
        for ch in word:
            node = node.setdefault(ch, {})
        node["#"] = True

    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(n):
        if not dp[i]:
            continue
        node = trie
        for j in range(i, n):
            if s[j] not in node:
                break
            node = node[s[j]]
            if "#" in node:
                dp[j + 1] = True

    return dp[n]


# ---------------------------------------------------------------------------
# Variant 2 — BFS
# ---------------------------------------------------------------------------

def word_break_bfs(s: str, word_dict: list[str]) -> bool:
    """
    Word break using BFS — positions are graph nodes.

    >>> word_break_bfs("leetcode", ["leet", "code"])
    True
    >>> word_break_bfs("applepenapple", ["apple", "pen"])
    True
    >>> word_break_bfs("catsandog", ["cats", "dog", "sand", "and", "cat"])
    False
    >>> word_break_bfs("", ["a"])
    True
    >>> word_break_bfs("aaaaaaa", ["aaaa", "aaa"])
    True
    """
    word_set = set(word_dict)
    n = len(s)
    visited = set()
    queue = deque([0])

    while queue:
        start = queue.popleft()
        if start == n:
            return True
        if start in visited:
            continue
        visited.add(start)
        for end in range(start + 1, n + 1):
            if s[start:end] in word_set:
                queue.append(end)

    return False


# ---------------------------------------------------------------------------
# Variant 3 — All segmentations (Word Break II)
# ---------------------------------------------------------------------------

def word_break_all_segs(s: str, word_dict: list[str]) -> list[str]:
    """
    Return all valid segmentations of s.

    >>> sorted(word_break_all_segs("catsanddog", ["cat", "cats", "and", "sand", "dog"]))
    ['cat sand dog', 'cats and dog']
    >>> word_break_all_segs("leetcode", ["leet", "code"])
    ['leet code']
    >>> word_break_all_segs("a", [])
    []
    """
    word_set = set(word_dict)

    @lru_cache(maxsize=None)
    def dp(start: int) -> list[str]:
        if start == len(s):
            return [""]
        results = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for rest in dp(end):
                    results.append(word + (" " + rest if rest else ""))
        return results

    result = dp(0)
    dp.cache_clear()
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("leetcode", ["leet", "code"], True),
    ("applepenapple", ["apple", "pen"], True),
    ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
    ("", ["a"], True),
    ("a", [], False),
    ("aaaaaaa", ["aaaa", "aaa"], True),
]

IMPLS = [
    ("reference", reference),
    ("trie", word_break_trie),
    ("bfs", word_break_bfs),
    ("all_segs", lambda s, d: len(word_break_all_segs(s, d)) > 0 if s else True),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for s, d, expected in TEST_CASES:
        results = {name: fn(s, d) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] s={s!r}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    # Show all segmentations
    segs = word_break_all_segs("catsanddog", ["cat", "cats", "and", "sand", "dog"])
    print(f"\n  All segmentations of 'catsanddog': {segs}")

    REPS = 20_000
    s_bench = "aaaaaaa"
    d_bench = ["aaaa", "aaa"]
    print(f"\n=== Benchmark: {REPS} runs, s={s_bench!r} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(s_bench, d_bench), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
