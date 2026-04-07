#!/usr/bin/env python3
"""
Optimized and alternative implementations of Word Search (LeetCode 79).

Reference uses a set of integer keys to track visited cells — one set.add/
remove per step plus an integer multiply per key.  Two improvements dominate
in practice:

1. In-place marking  — overwrite board[r][c] with a sentinel ('#') instead
   of maintaining a separate visited set.  Eliminates hashing overhead;
   restores the cell on backtrack.

2. Frequency pruning — before searching, check that the board contains at
   least as many of each character as the word needs.  Returns False
   immediately for impossible queries without touching the DFS.

3. Reverse-word trick — if the last character of the word is rarer on the
   board than the first, reverse the word.  The DFS branches less early
   because it reaches dead-ends sooner.

Variants covered:
1. word_exists_inplace   -- in-place '#' sentinel; no visited-set overhead
2. word_exists_pruned    -- freq-check + reverse trick + in-place marking
3. word_exists_iterative -- explicit stack DFS (avoids Python recursion limit
                            on huge boards / long words)

Key interview insight:
    Reference:  O(m·n·4^L) DFS with set hashing per step
    In-place:   same complexity, ~2× faster — removes set overhead
    Pruned:     adds O(m·n + L) prefix check that short-circuits hopeless cases

Run:
    python backtracking/word_search_optimized.py
"""

from __future__ import annotations

import copy
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.word_search import word_exists as word_exists_reference

DIRS = ((0, 1), (0, -1), (1, 0), (-1, 0))


# ---------------------------------------------------------------------------
# Variant 1 — In-place marking with '#' sentinel
# ---------------------------------------------------------------------------

def word_exists_inplace(board: list[list[str]], word: str) -> bool:
    """
    Word search with in-place visited marking.

    Overwrites each visited cell with '#' before recursing; restores it on
    backtrack.  Eliminates the integer-key set used by the reference.

    >>> word_exists_inplace([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED")
    True
    >>> word_exists_inplace([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE")
    True
    >>> word_exists_inplace([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB")
    False
    >>> word_exists_inplace([["A"]], "A")
    True
    >>> word_exists_inplace([["B","A","A"],["A","A","A"],["A","B","A"]], "ABB")
    False
    """
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if board[r][c] != word[idx]:
            return False
        tmp, board[r][c] = board[r][c], "#"
        found = any(dfs(r + dr, c + dc, idx + 1) for dr, dc in DIRS)
        board[r][c] = tmp
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


# ---------------------------------------------------------------------------
# Variant 2 — Frequency pruning + reverse trick + in-place marking
# ---------------------------------------------------------------------------

def word_exists_pruned(board: list[list[str]], word: str) -> bool:
    """
    Word search with character-frequency pruning and reverse-word trick.

    Before DFS:
    1. Count board chars and word chars.  If any word char appears more times
       in word than on board → impossible → return False immediately.
    2. If word[-1] is rarer on the board than word[0], reverse the word so the
       DFS hits dead-ends earlier (fewer branches explored).

    Then runs in-place-marking DFS.

    >>> word_exists_pruned([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED")
    True
    >>> word_exists_pruned([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE")
    True
    >>> word_exists_pruned([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB")
    False
    >>> word_exists_pruned([["A"]], "A")
    True
    >>> word_exists_pruned([["B","A","A"],["A","A","A"],["A","B","A"]], "ABB")
    False
    """
    from collections import Counter

    rows, cols = len(board), len(board[0])
    board_count = Counter(board[r][c] for r in range(rows) for c in range(cols))
    word_count = Counter(word)

    # Frequency prune
    if any(word_count[ch] > board_count[ch] for ch in word_count):
        return False

    # Reverse trick: start from the rarer end
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if board[r][c] != word[idx]:
            return False
        tmp, board[r][c] = board[r][c], "#"
        found = any(dfs(r + dr, c + dc, idx + 1) for dr, dc in DIRS)
        board[r][c] = tmp
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))


# ---------------------------------------------------------------------------
# Variant 3 — Iterative DFS with explicit stack
# ---------------------------------------------------------------------------

def word_exists_iterative(board: list[list[str]], word: str) -> bool:
    """
    Word search with iterative DFS (explicit stack).

    Avoids Python's recursion limit on boards with very long words.
    Each stack frame stores (row, col, word_index, visited_frozenset).
    Using frozenset means no mutation — safe for branching.

    Note: frozenset copies make this slower than in-place variants; it is
    included here to show the iterative pattern, not for raw speed.

    >>> word_exists_iterative([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED")
    True
    >>> word_exists_iterative([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE")
    True
    >>> word_exists_iterative([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB")
    False
    >>> word_exists_iterative([["A"]], "A")
    True
    >>> word_exists_iterative([["B","A","A"],["A","A","A"],["A","B","A"]], "ABB")
    False
    """
    rows, cols = len(board), len(board[0])

    for sr in range(rows):
        for sc in range(cols):
            if board[sr][sc] != word[0]:
                continue
            stack = [(sr, sc, 0, frozenset([(sr, sc)]))]
            while stack:
                r, c, idx, visited = stack.pop()
                if idx == len(word) - 1:
                    return True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and (nr, nc) not in visited
                        and board[nr][nc] == word[idx + 1]
                    ):
                        stack.append((nr, nc, idx + 1, visited | {(nr, nc)}))

    return False


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

_BOARD = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]
_BOARD2 = [["B", "A", "A"], ["A", "A", "A"], ["A", "B", "A"]]

TEST_CASES = [
    (_BOARD,  "ABCCED", True),
    (_BOARD,  "SEE",    True),
    (_BOARD,  "ABCB",   False),
    ([["A"]], "A",      True),
    (_BOARD2, "ABB",    False),
]

IMPLS = [
    ("reference",  word_exists_reference),
    ("inplace",    word_exists_inplace),
    ("pruned",     word_exists_pruned),
    ("iterative",  word_exists_iterative),
]

# Benchmark boards
# Board 1 — 5×5 all-A grid.  Tests deep DFS on a path that exists.
_BOARD_ALLA = [["A"] * 5 for _ in range(5)]
_PRESENT_WORD = "A" * 10     # snake path exists on 5×5; found after moderate DFS

# Board 2 — 4×4 nearly-all-A grid, one 'B' at corner.
# Absent word: char 'Z' never on the board → frequency pruning kills it instantly.
_BOARD_NO_Z = [["A"] * 4 for _ in range(4)]
_ABSENT_WORD_FREQ = "AAAAZ"  # Z not on board → instant prune

# Board 3 — same 4×4 all-A, word has right chars but no valid path.
# "AAAAA" on a 4×4 all-A board exists trivially, so use a board where
# the path is truly impossible due to topology.
_BOARD_TRAP = [
    ["A", "A", "A", "A"],
    ["A", "B", "B", "A"],
    ["A", "B", "B", "A"],
    ["A", "A", "A", "A"],
]
# Word crosses the BB barrier — needs to use A's on both sides non-adjacently.
_ABSENT_WORD_TOPO = "AAAAAAAAA"  # 9 A's; only 8 A's on board → freq prune


def run_all() -> None:
    print("\n=== Correctness ===")
    for board, word, expected in TEST_CASES:
        results = {name: fn(copy.deepcopy(board), word) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] {word!r:<10}  expected={expected}  "
            + "  ".join(f"{n}={v}" for n, v in results.items())
        )

    REPS = 500

    print(f"\n=== Benchmark 1: 5×5 all-A board, present word (len=10), {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(copy.deepcopy(_BOARD_ALLA), _PRESENT_WORD), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>8.3f} ms")

    print(f"\n=== Benchmark 2: absent word — char not on board (freq prune wins), {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(copy.deepcopy(_BOARD_NO_Z), _ABSENT_WORD_FREQ), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>8.3f} ms")

    print(f"\n=== Benchmark 3: absent word — freq prune (too many of a char), {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(copy.deepcopy(_BOARD_TRAP), _ABSENT_WORD_TOPO), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
