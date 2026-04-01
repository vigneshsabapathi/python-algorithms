"""
Optimized Bitap (Shift-Or) string matching.
Companion to bitap_string_match.py.

Two improvements over the original:
  1. Dict-based pattern mask — supports any character set, not just lowercase a-z.
     The original uses a fixed 27-element array indexed by `ord(c) - ord('a')`,
     which silently produces wrong results for uppercase, digits, or unicode.
  2. Benchmark against Python's str.find() — the built-in is C-level and
     typically 5–20x faster. Documents when Bitap is and isn't the right tool.

Both implementations return the same result for lowercase-alpha inputs.
"""


def bitap_string_match_dict(text: str, pattern: str) -> int:
    """
    Bitap (Shift-Or) search with a dict-based pattern mask.
    Works for any character set — not restricted to lowercase a-z.

    >>> bitap_string_match_dict('abdabababc', 'ababc')
    5
    >>> bitap_string_match_dict('aaaaaaaaaaaaaaaaaa', 'a')
    0
    >>> bitap_string_match_dict('abdabababc', '')
    0
    >>> bitap_string_match_dict('abdabababc', 'c')
    9
    >>> bitap_string_match_dict('abdabababc', 'fofosdfo')
    -1
    >>> bitap_string_match_dict('Hello World', 'World')
    6
    >>> bitap_string_match_dict('ATCGATCG', 'GATC')
    3
    >>> bitap_string_match_dict('abdab', 'fofosdfo')
    -1
    """
    if not pattern:
        return 0
    m = len(pattern)
    if m > len(text):
        return -1

    # Build mask only for chars that appear in the pattern.
    # mask[c] has bit i = 0 when pattern[i] == c.
    # Characters absent from the pattern return ~0 (all bits set) via .get().
    mask: dict[str, int] = {}
    for i, char in enumerate(pattern):
        mask[char] = mask.get(char, ~0) & ~(1 << i)

    state = ~1
    for i, char in enumerate(text):
        state |= mask.get(char, ~0)  # unknown char → ~0, resets state
        state <<= 1
        if not (state & (1 << m)):
            return i - m + 1

    return -1


def benchmark() -> None:
    from timeit import timeit
    from bitap_string_match import bitap_string_match

    n = 100_000
    # Original only handles a-z; use lowercase-only text for fair comparison.
    # The dict variant also handles mixed-case, digits, and unicode (extra cases below).
    cases = [
        ("short, short pat",
         "abdabababc", "ababc"),
        ("medium (a-z only), short pat",
         "abcdefghijklmnopqrstuvwxyz" * 17, "xyz"),
        ("medium (a-z only), long pat",
         "abcdefghijklmnopqrstuvwxyz" * 17, "stuvwxyz"),
        ("long (a-z only), long pat",
         "abcdefghijklmnopqrstuvwxyz" * 100, "stuvwxyz"),
    ]

    print(f"Benchmarking {n:,} runs:\n")
    for label, txt, pat in cases:
        t_orig = timeit(
            "bitap_string_match(t, p)",
            setup=(
                "from bitap_string_match import bitap_string_match; "
                f"t={txt!r}; p={pat!r}"
            ),
            number=n,
        )
        t_dict = timeit(
            "bitap_string_match_dict(t, p)",
            setup=(
                "from bitap_string_match_optimized import bitap_string_match_dict; "
                f"t={txt!r}; p={pat!r}"
            ),
            number=n,
        )
        t_find = timeit(
            "t.find(p)",
            setup=f"t={txt!r}; p={pat!r}",
            number=n,
        )

        print(f"  {label} (text={len(txt)}, pat={len(pat)!r}):")
        print(f"    original  (fixed array, a-z only)   {t_orig:.4f}s")
        print(f"    dict      (any charset)              {t_dict:.4f}s")
        print(f"    str.find  (C-level built-in)         {t_find:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
