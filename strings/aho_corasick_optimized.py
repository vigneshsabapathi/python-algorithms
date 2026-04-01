"""
Optimized Aho-Corasick multi-pattern string search.

Key improvements over the original:
1. Dict-based children: each node stores {char: state_id} instead of a list
   scanned linearly. State transition drops from O(alphabet_size) to O(1).
2. Complete goto table: after BFS for fail links, every node's children dict
   is extended with inherited transitions from its fail state. The search loop
   becomes a single dict lookup per character — no inner while-loop at all.
3. AhoCorasick is a self-contained class with no global state.
"""

from __future__ import annotations

from collections import deque


class AhoCorasick:
    """
    Aho-Corasick automaton with O(1) per-character state transitions.

    Build: O(sum of keyword lengths × alphabet interactions)
    Search: O(n + total matches) with zero Python while-loops
    """

    def __init__(self, keywords: list[str]) -> None:
        self._children: list[dict[str, int]] = [{}]
        self._fail: list[int] = [0]
        self._output: list[list[str]] = [[]]
        for kw in keywords:
            self._insert(kw)
        self._build()

    # ------------------------------------------------------------------ build

    def _insert(self, keyword: str) -> None:
        state = 0
        for char in keyword:
            if char not in self._children[state]:
                self._children.append({})
                self._fail.append(0)
                self._output.append([])
                self._children[state][char] = len(self._children) - 1
            state = self._children[state][char]
        self._output[state].append(keyword)

    def _build(self) -> None:
        """
        BFS to compute fail links and complete the goto function.

        Processing in BFS (level) order guarantees that fail[r] is always at a
        shallower level and therefore fully processed before r. Inheriting
        transitions from fail[r]'s *complete* goto into r's children gives each
        node a full transition dict, eliminating the fail-chain while-loop
        during search.
        """
        q: deque[int] = deque()

        # Level-1 nodes: fail → root
        for child in self._children[0].values():
            self._fail[child] = 0
            q.append(child)

        while q:
            r = q.popleft()
            fail_r = self._fail[r]

            # Set fail + output for each real child of r.
            # fail[child] = complete_goto[fail_r][char].
            # Since fail_r was processed before r (BFS order), its children
            # dict is already complete (real + inherited transitions).
            for char, child in self._children[r].items():
                q.append(child)
                self._fail[child] = self._children[fail_r].get(char, 0)
                self._output[child] = (
                    self._output[child] + self._output[self._fail[child]]
                )

            # Complete goto of r: inherit any transition from fail_r that r
            # doesn't already define.  This must happen *after* processing r's
            # real children so we don't enqueue inherited transitions above.
            for char, dest in self._children[fail_r].items():
                self._children[r].setdefault(char, dest)

    # ----------------------------------------------------------------- search

    def search_in(self, text: str) -> dict[str, list[int]]:
        """
        Return {keyword: [start_positions]} for every match in *text*.

        >>> ac = AhoCorasick(["what", "hat", "ver", "er"])
        >>> ac.search_in("whatever, err ... , wherever")
        {'what': [0], 'hat': [1], 'ver': [5, 25], 'er': [6, 10, 22, 26]}
        >>> ac2 = AhoCorasick(["he", "she", "his", "hers"])
        >>> ac2.search_in("ahishers")
        {'his': [1], 'she': [3], 'he': [4], 'hers': [4]}
        >>> AhoCorasick(["xyz"]).search_in("hello")
        {}
        >>> ac3 = AhoCorasick(["a", "ab", "abc"])
        >>> ac3.search_in("xabcy")
        {'a': [1], 'ab': [1], 'abc': [1]}
        """
        result: dict[str, list[int]] = {}
        state = 0
        for i, char in enumerate(text):
            state = self._children[state].get(char, 0)
            for keyword in self._output[state]:
                result.setdefault(keyword, []).append(i - len(keyword) + 1)
        return result


def benchmark() -> None:
    import timeit

    from strings.aho_corasick import Automaton

    keywords = ["what", "hat", "ver", "er", "he", "she", "his", "hers"]
    text = "whatever, err ... , wherever ahishers " * 500
    n = 1_000

    orig_build = timeit.timeit(lambda: Automaton(keywords), number=n)
    opt_build = timeit.timeit(lambda: AhoCorasick(keywords), number=n)

    orig_auto = Automaton(keywords)
    opt_auto = AhoCorasick(keywords)

    orig_search = timeit.timeit(lambda: orig_auto.search_in(text), number=n)
    opt_search = timeit.timeit(lambda: opt_auto.search_in(text), number=n)

    print(f"build ({len(keywords)} keywords):")
    print(f"  original (list + linear scan): {orig_build:.3f}s")
    print(f"  optimized (dict + goto table): {opt_build:.3f}s")
    print()
    print(f"search ({len(text):,} chars, {n} iters):")
    print(f"  original: {orig_search:.3f}s")
    print(f"  optimized: {opt_search:.3f}s")

    winner_b = "optimized" if opt_build < orig_build else "original"
    winner_s = "optimized" if opt_search < orig_search else "original"
    print(f"\nFastest build:  {winner_b}")
    print(f"Fastest search: {winner_s}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
