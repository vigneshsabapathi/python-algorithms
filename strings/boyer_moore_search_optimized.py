"""
Correct Boyer-Moore bad-character heuristic implementation.
Companion to boyer_moore_search.py.

Bug in the original:
    `i = mismatch_index - match_index` inside a Python for loop has NO EFFECT.
    Python's for-iterator resets `i` from the range on every iteration, so the
    shift is silently discarded. The original runs as O(n*m) brute force.

Two fixes applied here:
    1. Use a while loop so the shift variable `s` is actually advanced.
    2. Pre-build the bad-character table in __init__ — O(1) hash lookup instead
       of O(m) linear scan through the pattern on every mismatch.
"""


class BoyerMooreSearchFast:
    """
    Boyer-Moore search using bad-character heuristic with:
      - while loop so shifts actually take effect
      - dict-based bad-character table built once at init (O(1) lookup)

    Example:
        bms = BoyerMooreSearchFast(text="ABAABA", pattern="AB")
        bms.bad_character_heuristic()   # [0, 3]
    """

    def __init__(self, text: str, pattern: str):
        self.text = text
        self.pattern = pattern
        # bad_char[c] = last index of character c in pattern.
        # Built in O(m); lookup is O(1) vs O(m) linear scan in the original.
        self._bad_char: dict[str, int] = {c: i for i, c in enumerate(pattern)}

    def bad_character_heuristic(self) -> list[int]:
        """
        Returns all start positions where pattern occurs in text.
        Uses while loop so shift variable is actually updated.

        >>> BoyerMooreSearchFast("ABAABA", "AB").bad_character_heuristic()
        [0, 3]
        >>> BoyerMooreSearchFast("AABAACAADAABAABA", "AABA").bad_character_heuristic()
        [0, 9, 12]
        >>> BoyerMooreSearchFast("ABCABC", "ABC").bad_character_heuristic()
        [0, 3]
        >>> BoyerMooreSearchFast("AAAA", "AA").bad_character_heuristic()
        [0, 1, 2]
        >>> BoyerMooreSearchFast("ABCDEF", "XYZ").bad_character_heuristic()
        []
        >>> BoyerMooreSearchFast("", "AB").bad_character_heuristic()
        []
        >>> BoyerMooreSearchFast("AB", "").bad_character_heuristic()
        []
        """
        text, pattern = self.text, self.pattern
        n, m = len(text), len(pattern)
        if m == 0 or n < m:
            return []

        positions = []
        s = 0  # current alignment shift — updated by actual heuristic
        while s <= n - m:
            j = m - 1  # compare right to left

            while j >= 0 and pattern[j] == text[s + j]:
                j -= 1

            if j < 0:
                # Full match at position s
                positions.append(s)
                s += 1  # advance past match (good-suffix rule would be bigger)
            else:
                # Bad character: find last occurrence of text[s+j] in pattern
                bad_char_pos = self._bad_char.get(text[s + j], -1)
                # Shift pattern right so the bad char aligns with its last
                # occurrence in pattern. At minimum shift by 1 to avoid stalling.
                s += max(1, j - bad_char_pos)

        return positions


# ---------------------------------------------------------------------------
# Standalone functional version (no class overhead)
# ---------------------------------------------------------------------------

def boyer_moore_search(text: str, pattern: str) -> list[int]:
    """
    Functional Boyer-Moore bad-character search. Same algorithm as
    BoyerMooreSearchFast but without class wrapper — slightly faster.

    >>> boyer_moore_search("ABAABA", "AB")
    [0, 3]
    >>> boyer_moore_search("AABAACAADAABAABA", "AABA")
    [0, 9, 12]
    >>> boyer_moore_search("ABCDEF", "XYZ")
    []
    >>> boyer_moore_search("", "AB")
    []
    >>> boyer_moore_search("AB", "")
    []
    """
    n, m = len(text), len(pattern)
    if m == 0 or n < m:
        return []

    bad_char = {c: i for i, c in enumerate(pattern)}
    positions = []
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            positions.append(s)
            s += 1
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
    return positions


# ---------------------------------------------------------------------------
# Benchmark — shows O(n*m) vs O(n/m) impact at scale
# ---------------------------------------------------------------------------

def benchmark() -> None:
    from timeit import timeit

    n = 5_000

    # Boyer-Moore shines when pattern is long and text has rare characters
    text_dna = "ACGTACGTACGTTTTTACGTACGTACGT" * 100          # 2800 chars
    text_text = "the quick brown fox jumps over the lazy dog " * 50  # 2200 chars

    cases = [
        ("DNA, short pattern",  text_dna,  "ACGT"),
        ("DNA, long pattern",   text_dna,  "ACGTACGTACGTTTTT"),
        ("English, short pat",  text_text, "fox"),
        ("English, long pat",   text_text, "quick brown fox"),
    ]

    print(f"Benchmarking {n:,} runs:\n")
    for label, txt, pat in cases:
        t_orig = timeit(
            "BoyerMooreSearch(t, p).bad_character_heuristic()",
            setup=(
                "from boyer_moore_search import BoyerMooreSearch; "
                f"t={txt!r}; p={pat!r}"
            ),
            number=n,
        )
        t_cls = timeit(
            "BoyerMooreSearchFast(t, p).bad_character_heuristic()",
            setup=(
                "from boyer_moore_search_optimized import BoyerMooreSearchFast; "
                f"t={txt!r}; p={pat!r}"
            ),
            number=n,
        )
        t_fn = timeit(
            "boyer_moore_search(t, p)",
            setup=(
                "from boyer_moore_search_optimized import boyer_moore_search; "
                f"t={txt!r}; p={pat!r}"
            ),
            number=n,
        )

        print(f"  {label} (text={len(txt)}, pat={len(pat)!r}):")
        print(f"    original  (for loop, O(n*m) brute force)  {t_orig:.4f}s")
        print(f"    class     (while loop, O(1) table lookup)  {t_cls:.4f}s")
        print(f"    functional (no class overhead)             {t_fn:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
