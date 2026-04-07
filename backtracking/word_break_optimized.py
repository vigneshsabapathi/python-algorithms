#!/usr/bin/env python3
"""
Optimized and alternative implementations of Word Break.

The reference backtracking explores every substring split without caching —
the same suffix can be re-evaluated many times on different paths, giving
O(2^n) worst-case time.

Variants covered:
1. word_break_memo    -- Top-down backtracking + memoization (functools.cache).
                         Each index is solved at most once: O(n^2) time, O(n) space.
2. word_break_dp      -- Bottom-up DP table.  dp[i] = True iff s[:i] can be
                         segmented.  Classic O(n^2) / O(n) interview answer.
3. word_break_bfs     -- BFS over valid split indices.  Equivalent to DP but
                         framed as a graph-reachability problem.
4. word_break_trie    -- Trie prefix pruning.  Limits inner loop to at most
                         max_word_len steps AND prunes as soon as no word in the
                         dict starts with the current prefix — useful when the
                         dict contains very long words.

Key interview insight:
    Backtracking (no memo): O(2^n)  — re-explores shared suffixes
    Memo / DP / BFS:        O(n^2)  — each index resolved once
    Trie + DP:              O(n * L) — L = max word length (often << n)

Run:
    python backtracking/word_break_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.word_break import word_break as word_break_reference


# ---------------------------------------------------------------------------
# Variant 1 — Top-down memoization
# ---------------------------------------------------------------------------

def word_break_memo(input_string: str, word_dict: set[str]) -> bool:
    """
    Word break with top-down memoization.

    Wraps the recursive backtracking helper with @lru_cache so each starting
    index is computed at most once.  Reduces worst-case from O(2^n) to O(n^2).

    >>> word_break_memo("leetcode", {"leet", "code"})
    True
    >>> word_break_memo("applepenapple", {"apple", "pen"})
    True
    >>> word_break_memo("catsandog", {"cats", "dog", "sand", "and", "cat"})
    False
    >>> word_break_memo("applepenapple", set())
    False
    >>> word_break_memo("", {"any"})
    True
    """
    frozen = frozenset(word_dict)

    @lru_cache(maxsize=None)
    def dp(start: int) -> bool:
        if start == len(input_string):
            return True
        for end in range(start + 1, len(input_string) + 1):
            if input_string[start:end] in frozen and dp(end):
                return True
        return False

    return dp(0)


# ---------------------------------------------------------------------------
# Variant 2 — Bottom-up DP
# ---------------------------------------------------------------------------

def word_break_dp(input_string: str, word_dict: set[str]) -> bool:
    """
    Word break with bottom-up dynamic programming.

    dp[i] is True iff input_string[:i] can be segmented into dict words.
    Transition: dp[i] = any(dp[j] and input_string[j:i] in word_dict)
    for j in 0..i-1.

    Time: O(n^2)  Space: O(n)

    >>> word_break_dp("leetcode", {"leet", "code"})
    True
    >>> word_break_dp("applepenapple", {"apple", "pen"})
    True
    >>> word_break_dp("catsandog", {"cats", "dog", "sand", "and", "cat"})
    False
    >>> word_break_dp("applepenapple", set())
    False
    >>> word_break_dp("", {"any"})
    True
    """
    n = len(input_string)
    dp = [False] * (n + 1)
    dp[0] = True  # empty prefix is always segmentable

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and input_string[j:i] in word_dict:
                dp[i] = True
                break

    return dp[n]


# ---------------------------------------------------------------------------
# Variant 3 — BFS over reachable indices
# ---------------------------------------------------------------------------

def word_break_bfs(input_string: str, word_dict: set[str]) -> bool:
    """
    Word break with BFS.

    Treat each index as a node.  Start at 0, extend by any dict word from
    the current position, enqueue the resulting index.  Reach n = success.

    Same O(n^2) complexity as DP but framed as graph reachability —
    useful for returning *all* valid segmentations (just track paths).

    >>> word_break_bfs("leetcode", {"leet", "code"})
    True
    >>> word_break_bfs("applepenapple", {"apple", "pen"})
    True
    >>> word_break_bfs("catsandog", {"cats", "dog", "sand", "and", "cat"})
    False
    >>> word_break_bfs("applepenapple", set())
    False
    >>> word_break_bfs("", {"any"})
    True
    """
    from collections import deque

    n = len(input_string)
    visited: set[int] = {0}
    queue: deque[int] = deque([0])

    while queue:
        start = queue.popleft()
        for end in range(start + 1, n + 1):
            if end not in visited and input_string[start:end] in word_dict:
                if end == n:
                    return True
                visited.add(end)
                queue.append(end)

    return n == 0  # empty string edge case


# ---------------------------------------------------------------------------
# Variant 4 — Trie + DP (bounds inner loop to max_word_len)
# ---------------------------------------------------------------------------

class _TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.is_end: bool = False


def _build_trie(word_dict: set[str]) -> _TrieNode:
    root = _TrieNode()
    for word in word_dict:
        node = root
        for ch in word:
            node = node.children.setdefault(ch, _TrieNode())
        node.is_end = True
    return root


def word_break_trie(input_string: str, word_dict: set[str]) -> bool:
    """
    Word break with Trie-accelerated DP.

    For each DP position i, walk the trie from input_string[i] forward.
    Stop as soon as no trie edge matches (prefix not in any word) — avoids
    scanning positions that can never complete a word.

    Worst-case O(n * L) where L = max word length.  Practical advantage over
    plain DP when the dictionary has many short words with few shared prefixes.

    >>> word_break_trie("leetcode", {"leet", "code"})
    True
    >>> word_break_trie("applepenapple", {"apple", "pen"})
    True
    >>> word_break_trie("catsandog", {"cats", "dog", "sand", "and", "cat"})
    False
    >>> word_break_trie("applepenapple", set())
    False
    >>> word_break_trie("", {"any"})
    True
    """
    root = _build_trie(word_dict)
    n = len(input_string)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(n):
        if not dp[i]:
            continue
        node = root
        for j in range(i, n):
            ch = input_string[j]
            if ch not in node.children:
                break  # no word in dict starts with input_string[i:j+1]
            node = node.children[ch]
            if node.is_end:
                dp[j + 1] = True

    return dp[n]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("leetcode",      {"leet", "code"},                      True),
    ("applepenapple", {"apple", "pen"},                      True),
    ("catsandog",     {"cats", "dog", "sand", "and", "cat"}, False),
    ("applepenapple", set(),                                  False),
    ("",              {"any"},                                True),
    ("ab",            {"a", "b"},                            True),
    # pathological: long string that forces backtracking to re-explore
    ("a" * 20 + "b",  {"a", "aa", "aaa", "aaaa"},            False),
]

IMPLS = [
    ("reference",   word_break_reference),
    ("memo",        word_break_memo),
    ("dp",          word_break_dp),
    ("bfs",         word_break_bfs),
    ("trie",        word_break_trie),
]

# Benchmark input: worst-case for backtracking (all-a string with no valid break)
# 20 chars → ~2^20 paths for pure backtracking; manageable in small reps
_BENCH_S = "a" * 20 + "b"
_BENCH_D = {"a", "aa", "aaa", "aaaa", "aaaaa"}


def run_all() -> None:
    print("\n=== Correctness ===")
    for s, d, expected in TEST_CASES:
        results = {name: fn(s, d) for name, fn in IMPLS}
        all_correct = all(v == expected for v in results.values())
        tag = "OK" if all_correct else "FAIL"
        print(f"  [{tag}] {s!r:25s}  expected={expected}  "
              + "  ".join(f"{n}={v}" for n, v in results.items()))

    # Reference is exponential on worst-case; use fewer reps to keep runtime sane
    REPS_SLOW = 3
    REPS_FAST = 500
    print(f"\n=== Benchmark: worst-case string len={len(_BENCH_S)} ===")
    for name, fn in IMPLS:
        reps = REPS_SLOW if name == "reference" else REPS_FAST
        t = timeit.timeit(lambda fn=fn: fn(_BENCH_S, _BENCH_D), number=reps) * 1000 / reps
        label = f"({reps} runs)"
        print(f"  {name:<12} {t:>9.3f} ms  {label}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
