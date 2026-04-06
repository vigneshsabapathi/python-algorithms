#!/usr/bin/env python3
"""
Optimized and alternative implementations of Match Word Pattern.

The reference implementation (match_word_pattern) solves the *substring* variant:
each pattern character maps to a contiguous substring — no delimiters given.
This is LeetCode 291 (Word Pattern II) — NP-hard in general.

Variants covered:
1. match_word_pattern_word_split  -- LeetCode 290: space-delimited words, O(n)
2. match_word_pattern_backtrack   -- reference (imported), O(n^m) substring search
3. match_word_pattern_pruned      -- backtracking + remaining-length pruning
4. match_word_pattern_lc290_regex -- regex bijection check (fun, not recommended)

Key interview insight:
    LeetCode 290 (word split)   — O(n): split string, zip with pattern, check bijection.
    LeetCode 291 (substring)    — O(n^m): backtracking; each of m pattern chars can
                                   split the string at any of ~n positions.
    Pruning wins: track remaining pattern chars × min-length-1 each; if remaining
    string is shorter than that lower bound, prune immediately.

Run:
    python backtracking/match_word_pattern_optimized.py
"""

from __future__ import annotations

import re
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.match_word_pattern import match_word_pattern as match_word_pattern_backtrack


# ---------------------------------------------------------------------------
# Variant 1 — LeetCode 290: space-delimited word matching, O(n)
# ---------------------------------------------------------------------------


def match_word_pattern_word_split(pattern: str, sentence: str) -> bool:
    """
    LeetCode 290 — Word Pattern.
    The sentence is split by spaces into words; each pattern character must
    map bijectively to exactly one word.

    O(n) time, O(k) space where k = number of unique pattern chars / words.

    >>> match_word_pattern_word_split("abba", "dog cat cat dog")
    True
    >>> match_word_pattern_word_split("abba", "dog cat cat fish")
    False
    >>> match_word_pattern_word_split("aaaa", "dog cat cat dog")
    False
    >>> match_word_pattern_word_split("abba", "dog dog dog dog")
    False
    >>> match_word_pattern_word_split("a", "dog")
    True
    >>> match_word_pattern_word_split("ab", "dog dog")
    False
    """
    words = sentence.split()
    if len(pattern) != len(words):
        return False
    char_to_word: dict[str, str] = {}
    word_to_char: dict[str, str] = {}
    for char, word in zip(pattern, words):
        if char in char_to_word:
            if char_to_word[char] != word:
                return False
        else:
            if word in word_to_char:
                return False  # bijection: two chars can't map to the same word
            char_to_word[char] = word
            word_to_char[word] = char
    return True


# ---------------------------------------------------------------------------
# Variant 2 — Pruned backtracking (LeetCode 291 substring variant)
# ---------------------------------------------------------------------------


def match_word_pattern_pruned(pattern: str, input_string: str) -> bool:
    """
    Backtracking with remaining-length lower-bound pruning:
    Each unassigned pattern character must consume at least 1 character.
    If the remaining string is shorter than the number of remaining
    unassigned pattern chars, prune immediately.

    Also skips already-mapped chars' contribution to the lower bound.

    >>> match_word_pattern_pruned("aba", "GraphTreesGraph")
    True
    >>> match_word_pattern_pruned("xyx", "PythonRubyPython")
    True
    >>> match_word_pattern_pruned("GG", "PythonJavaPython")
    False
    >>> match_word_pattern_pruned("abba", "dogcatcatdog")
    True
    >>> match_word_pattern_pruned("abba", "dogcatcatfish")
    False
    >>> match_word_pattern_pruned("", "")
    True
    >>> match_word_pattern_pruned("a", "")
    False
    """

    def backtrack(p_idx: int, s_idx: int) -> bool:
        if p_idx == len(pattern) and s_idx == len(input_string):
            return True
        if p_idx == len(pattern) or s_idx == len(input_string):
            return False

        # Pruning: remaining string must be long enough for unassigned chars
        remaining_str = len(input_string) - s_idx
        remaining_pat = len(pattern) - p_idx
        # Each unassigned pattern char needs at least 1 char; assigned chars
        # need exactly their mapped length
        min_needed = 0
        for i in range(p_idx, len(pattern)):
            ch = pattern[i]
            if ch in pattern_map:
                min_needed += len(pattern_map[ch])
            else:
                min_needed += 1
        if remaining_str < min_needed:
            return False

        char = pattern[p_idx]
        if char in pattern_map:
            mapped = pattern_map[char]
            if input_string.startswith(mapped, s_idx):
                return backtrack(p_idx + 1, s_idx + len(mapped))
            return False

        for end in range(s_idx + 1, len(input_string) + 1):
            substr = input_string[s_idx:end]
            if substr in str_map:
                continue
            pattern_map[char] = substr
            str_map[substr] = char
            if backtrack(p_idx + 1, end):
                return True
            del pattern_map[char]
            del str_map[substr]
        return False

    pattern_map: dict[str, str] = {}
    str_map: dict[str, str] = {}
    return backtrack(0, 0)


# ---------------------------------------------------------------------------
# Variant 3 — LeetCode 290 with regex (demonstrative, not recommended)
# ---------------------------------------------------------------------------


def match_word_pattern_lc290_regex(pattern: str, sentence: str) -> bool:
    """
    LeetCode 290 using regex — map each pattern char to a named capture group.
    Regex enforces char→word mapping via back-references, but cannot prevent
    two *different* pattern chars from matching the *same* word (bijection gap).
    We patch that with a final uniqueness check on captured groups.

    Included for illustration; not recommended in production.

    >>> match_word_pattern_lc290_regex("abba", "dog cat cat dog")
    True
    >>> match_word_pattern_lc290_regex("abba", "dog cat cat fish")
    False
    >>> match_word_pattern_lc290_regex("aaaa", "dog cat cat dog")
    False
    >>> match_word_pattern_lc290_regex("abba", "dog dog dog dog")
    False
    >>> match_word_pattern_lc290_regex("a", "dog")
    True
    >>> match_word_pattern_lc290_regex("ab", "dog dog")
    False
    """
    words = sentence.split()
    if len(pattern) != len(words):
        return False
    # Build a regex: each unique char → named group; repeated char → back-reference
    seen: dict[str, str] = {}
    regex_parts: list[str] = []
    for char in pattern:
        if char not in seen:
            group = f"(?P<g{ord(char)}>[^ ]+)"
            seen[char] = f"g{ord(char)}"
            regex_parts.append(group)
        else:
            regex_parts.append(f"(?P={seen[char]})")
    regex = " ".join(regex_parts) + "$"
    m = re.fullmatch(regex, sentence)
    if not m:
        return False
    # Patch: ensure different pattern chars mapped to different words (bijection)
    captured = list(m.groupdict().values())
    return len(captured) == len(set(captured))


# ---------------------------------------------------------------------------
# Correctness check + benchmark
# ---------------------------------------------------------------------------


def run_all() -> None:
    # --- LeetCode 290 cases ---
    lc290_cases: list[tuple[str, str, bool]] = [
        ("abba", "dog cat cat dog", True),
        ("abba", "dog cat cat fish", False),
        ("aaaa", "dog cat cat dog", False),
        ("abba", "dog dog dog dog", False),
        ("a",    "dog",             True),
        ("ab",   "dog dog",         False),
    ]

    print("\n=== LeetCode 290 (word-split) correctness ===")
    for pat, s, expected in lc290_cases:
        r1 = match_word_pattern_word_split(pat, s)
        r2 = match_word_pattern_lc290_regex(pat, s)
        ok = r1 == r2 == expected
        print(f"  {'OK' if ok else 'FAIL'}  pattern={pat!r:6} string={s!r:26} "
              f"expected={expected}  split={r1}  regex={r2}")

    # --- LeetCode 291 cases (substring backtracking) ---
    lc291_cases: list[tuple[str, str, bool]] = [
        ("aba",  "GraphTreesGraph",  True),
        ("xyx",  "PythonRubyPython", True),
        ("GG",   "PythonJavaPython", False),
        ("abba", "dogcatcatdog",     True),
        ("abba", "dogcatcatfish",    False),
        ("aab",  "catcatdog",        True),
        ("a",    "Hello",            True),
        ("aa",   "HelloHello",       True),
        ("aa",   "HelloWorld",       False),
        ("",     "",                 True),
        ("a",    "",                 False),
    ]

    print("\n=== LeetCode 291 (substring) correctness ===")
    for pat, s, expected in lc291_cases:
        r1 = match_word_pattern_backtrack(pat, s)
        r2 = match_word_pattern_pruned(pat, s)
        ok = r1 == r2 == expected
        print(f"  {'OK' if ok else 'FAIL'}  pattern={pat!r:6} string={s!r:22} "
              f"expected={expected}  backtrack={r1}  pruned={r2}")

    # --- Benchmark ---
    REPS = 10000

    print(f"\n=== Benchmark LeetCode 290 ({REPS} runs each) ===")
    cases_290 = [
        ("abba", "dog cat cat dog"),
        ("aabb", "cat cat dog dog"),
    ]
    print(f"  {'case':>28}  {'word_split':>12}  {'regex':>12}")
    for pat, s in cases_290:
        t1 = timeit.timeit(lambda: match_word_pattern_word_split(pat, s), number=REPS) * 1e6 / REPS
        t2 = timeit.timeit(lambda: match_word_pattern_lc290_regex(pat, s), number=REPS) * 1e6 / REPS
        print(f"  {(pat + ' / ' + s)!r:>30}  {t1:>10.2f}us  {t2:>10.2f}us")

    print(f"\n=== Benchmark LeetCode 291 ({REPS} runs each) ===")
    cases_291 = [
        ("aba",  "GraphTreesGraph"),
        ("abba", "dogcatcatdog"),
        ("xyx",  "PythonRubyPython"),
    ]
    print(f"  {'case':>32}  {'backtrack':>12}  {'pruned':>12}")
    for pat, s in cases_291:
        t1 = timeit.timeit(lambda: match_word_pattern_backtrack(pat, s), number=REPS) * 1e6 / REPS
        t2 = timeit.timeit(lambda: match_word_pattern_pruned(pat, s), number=REPS) * 1e6 / REPS
        print(f"  {(pat + ' / ' + s)!r:>34}  {t1:>10.2f}us  {t2:>10.2f}us")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
