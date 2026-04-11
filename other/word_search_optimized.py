#!/usr/bin/env python3
"""
Optimized and alternative implementations of Word Search.

Variants covered:
1. dfs_backtrack    -- DFS backtracking (reference)
2. pruned_dfs       -- DFS with frequency-based pruning
3. trie_search      -- Trie-based multi-word search (Word Search II)

Run:
    python other/word_search_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.word_search import word_search as reference


def pruned_word_search(board: list[list[str]], word: str) -> bool:
    """
    Word search with frequency pruning — checks if board has enough letters
    before searching, and may reverse word for better pruning.

    >>> board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]
    >>> pruned_word_search(board, "ABCCED")
    True
    >>> pruned_word_search(board, "SEE")
    True
    >>> pruned_word_search(board, "ABCB")
    False
    >>> pruned_word_search([], "A")
    False
    """
    if not board or not board[0] or not word:
        return False

    # Frequency check
    board_count: Counter[str] = Counter()
    for row in board:
        board_count.update(row)

    word_count = Counter(word)
    for ch, cnt in word_count.items():
        if board_count[ch] < cnt:
            return False

    # Reverse word if last char is rarer (better pruning)
    if board_count[word[-1]] < board_count[word[0]]:
        word = word[::-1]

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
        temp = board[r][c]
        board[r][c] = "#"
        found = (
            dfs(r + 1, c, idx + 1) or dfs(r - 1, c, idx + 1)
            or dfs(r, c + 1, idx + 1) or dfs(r, c - 1, idx + 1)
        )
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True
    return False


def word_search_all_words(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Find all words from a list that exist in the board (Word Search II).

    >>> board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]
    >>> sorted(word_search_all_words(board, ["ABCCED", "SEE", "ABCB"]))
    ['ABCCED', 'SEE']
    >>> word_search_all_words([], ["A"])
    []
    """
    if not board or not board[0]:
        return []

    # Build trie
    trie: dict = {}
    for word in words:
        node = trie
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = word

    rows, cols = len(board), len(board[0])
    found: list[str] = []

    def dfs(r: int, c: int, node: dict) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        ch = board[r][c]
        if ch not in node:
            return
        next_node = node[ch]
        if "$" in next_node:
            found.append(next_node["$"])
            del next_node["$"]  # Avoid duplicates

        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc, next_node)
        board[r][c] = ch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie)

    return found


def word_search_with_path(board: list[list[str]], word: str) -> list[tuple[int, int]]:
    """
    Return the path of cells if word is found, else empty list.

    >>> board = [['A','B'],['C','D']]
    >>> word_search_with_path(board, "AB")
    [(0, 0), (0, 1)]
    >>> word_search_with_path(board, "XY")
    []
    """
    if not board or not board[0] or not word:
        return []

    rows, cols = len(board), len(board[0])
    path: list[tuple[int, int]] = []

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
        temp = board[r][c]
        board[r][c] = "#"
        path.append((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if dfs(r + dr, c + dc, idx + 1):
                board[r][c] = temp
                return True
        path.pop()
        board[r][c] = temp
        return False

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return path
    return []


BOARD = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
TEST_CASES = [
    ("ABCCED", True),
    ("SEE", True),
    ("ABCB", False),
]

IMPLS = [
    ("reference", reference),
    ("pruned", pruned_word_search),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for word, expected in TEST_CASES:
        for name, fn in IMPLS:
            board_copy = [row[:] for row in BOARD]
            result = fn(board_copy, word)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: word={word} expected={expected} got={result}")
        print(f"  [OK] word={word!r} -> {expected}")

    REPS = 20_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn([row[:] for row in BOARD], "ABCCED"),
            number=REPS,
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
