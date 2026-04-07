"""
Word Ladder — Optimized implementations.

Variants:
1. BFS (shortest path — LeetCode standard)
2. Bidirectional BFS (meets in the middle — fastest for large word lists)
3. BFS with wildcard pattern matching (generic word length)

Word Ladder: transform begin_word to end_word by changing one letter at a time,
each intermediate must be in the word list. Find shortest transformation.

Reference: LeetCode 127 — Word Ladder
"""

from __future__ import annotations

import string
from collections import deque


# ── Utility: generate neighbors of a word ────────────────────────────────


def _neighbors(word: str) -> set[str]:
    """Generate all words that differ from `word` by exactly one character."""
    result = set()
    for i in range(len(word)):
        for c in string.ascii_lowercase:
            if c != word[i]:
                result.add(word[:i] + c + word[i + 1 :])
    return result


# ── Variant 1: BFS (shortest path) ───────────────────────────────────────


def word_ladder_bfs(
    begin_word: str, end_word: str, word_list: list[str]
) -> list[str]:
    """
    BFS to find the shortest transformation from begin_word to end_word.

    Returns the actual path (not just the length). BFS guarantees
    the first path found is the shortest.

    >>> len(word_ladder_bfs("hit", "cog", ["hot","dot","dog","lot","log","cog"]))
    5
    >>> word_ladder_bfs("hit", "cog", ["hot","dot","dog","lot","log"])
    []
    >>> word_ladder_bfs("lead", "gold", ["load","goad","gold","lead","lord"])
    ['lead', 'load', 'goad', 'gold']
    >>> word_ladder_bfs("game", "code", ["came","cage","code","cade","gave"])
    ['game', 'came', 'cade', 'code']
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return []

    # queue stores (word, path)
    queue: deque[tuple[str, list[str]]] = deque()
    queue.append((begin_word, [begin_word]))
    visited: set[str] = {begin_word}

    while queue:
        current, path = queue.popleft()
        if current == end_word:
            return path
        for neighbor in _neighbors(current):
            if neighbor in word_set and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []


def word_ladder_bfs_length(
    begin_word: str, end_word: str, word_list: list[str]
) -> int:
    """
    BFS to find just the shortest path length (LeetCode 127 style).
    More memory-efficient than tracking full paths.

    >>> word_ladder_bfs_length("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5
    >>> word_ladder_bfs_length("hit", "cog", ["hot","dot","dog","lot","log"])
    0
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue: deque[tuple[str, int]] = deque()
    queue.append((begin_word, 1))
    visited: set[str] = {begin_word}

    while queue:
        current, length = queue.popleft()
        if current == end_word:
            return length
        for neighbor in _neighbors(current):
            if neighbor in word_set and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, length + 1))

    return 0


# ── Variant 2: Bidirectional BFS ─────────────────────────────────────────


def word_ladder_bibfs_length(
    begin_word: str, end_word: str, word_list: list[str]
) -> int:
    """
    Bidirectional BFS: search from both ends simultaneously.
    When the frontiers meet, the shortest path is found.
    Reduces search space from O(b^d) to O(b^(d/2)).

    >>> word_ladder_bibfs_length("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5
    >>> word_ladder_bibfs_length("hit", "cog", ["hot","dot","dog","lot","log"])
    0
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    front: set[str] = {begin_word}
    back: set[str] = {end_word}
    visited: set[str] = {begin_word, end_word}
    length = 2  # begin and end are already counted

    while front and back:
        # Always expand the smaller frontier
        if len(front) > len(back):
            front, back = back, front

        next_front: set[str] = set()
        for word in front:
            for neighbor in _neighbors(word):
                if neighbor in back:
                    return length
                if neighbor in word_set and neighbor not in visited:
                    visited.add(neighbor)
                    next_front.add(neighbor)
        front = next_front
        length += 1

    return 0


# ── Variant 3: BFS with wildcard patterns ────────────────────────────────


def word_ladder_pattern(
    begin_word: str, end_word: str, word_list: list[str]
) -> int:
    """
    BFS using wildcard pattern adjacency instead of generating all
    26-neighbor mutations. Build a map: h*t -> [hot, hit, ...].

    More efficient when words are long (avoids O(26 * len) neighbor generation
    at each step). Preprocessing is O(n * len).

    >>> word_ladder_pattern("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5
    >>> word_ladder_pattern("hit", "cog", ["hot","dot","dog","lot","log"])
    0
    """
    if end_word not in word_list:
        return 0

    # Build wildcard pattern map
    from collections import defaultdict

    patterns: dict[str, list[str]] = defaultdict(list)
    for word in word_list:
        for i in range(len(word)):
            pattern = word[:i] + "*" + word[i + 1 :]
            patterns[pattern].append(word)

    queue: deque[tuple[str, int]] = deque()
    queue.append((begin_word, 1))
    visited: set[str] = {begin_word}

    while queue:
        current, length = queue.popleft()
        if current == end_word:
            return length
        for i in range(len(current)):
            pattern = current[:i] + "*" + current[i + 1 :]
            for neighbor in patterns.get(pattern, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, length + 1))

    return 0


if __name__ == "__main__":
    import time

    # Standard test cases
    cases = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),
        ("lead", "gold", ["load", "goad", "gold", "lead", "lord"]),
        ("game", "code", ["came", "cage", "code", "cade", "gave"]),
    ]

    print("=== Correctness ===")
    for begin, end, words in cases:
        result = word_ladder_bfs(begin, end, words)
        length = word_ladder_bfs_length(begin, end, words)
        bibfs = word_ladder_bibfs_length(begin, end, words)
        pat = word_ladder_pattern(begin, end, words)
        print(f"  {begin} -> {end}: path={result} len={length} bibfs={bibfs} pattern={pat}")

    # Benchmark with larger word list
    import random

    print("\n=== Benchmark (random 4-letter words, 1000 word list) ===")
    random.seed(42)
    words_1k = list({"{:04d}".format(i) for i in range(1000)})
    # Create a realizable path
    begin, end = "0000", "9999"

    for name, fn in [
        ("BFS length", word_ladder_bfs_length),
        ("BiBFS length", word_ladder_bibfs_length),
        ("Pattern BFS", word_ladder_pattern),
    ]:
        t = time.perf_counter()
        result = fn(begin, end, words_1k)
        elapsed = time.perf_counter() - t
        print(f"  {name}: {result} ({elapsed:.6f}s)")

    import doctest
    doctest.testmod()
