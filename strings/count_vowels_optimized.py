"""
Optimized vowel counting implementations.
Companion to count_vowels.py.

Three approaches:
  1. Original: generator + string membership  — O(10n) linear scan per char
  2. frozenset: generator + hash lookup       — O(n) hash lookup per char
  3. translate+len: C-level delete non-vowels — O(n) entirely in C (ASCII strings)

Key insight: `char in "aeiouAEIOU"` scans a 10-char string on every character.
A frozenset gives O(1) hash lookup. For longer strings, translate runs entirely
in C and outperforms both Python-level approaches.
"""

# Module-level constants — built once, reused across all calls
_VOWELS: frozenset[str] = frozenset("aeiouAEIOU")

# Delete table: maps every ASCII non-vowel character to None (deletion)
# translate() then removes them in one C-level pass, leaving only vowels.
_ALL_ASCII = {chr(i) for i in range(128)}
_DELETE_NON_VOWELS = str.maketrans("", "", "".join(_ALL_ASCII - _VOWELS))


def count_vowels_frozenset(s: str) -> int:
    """
    Count vowels using frozenset membership — O(1) hash lookup per character
    instead of O(10) linear scan over the vowel string.

    >>> count_vowels_frozenset("hello world")
    3
    >>> count_vowels_frozenset("HELLO WORLD")
    3
    >>> count_vowels_frozenset("")
    0
    >>> count_vowels_frozenset("PYTHON")
    1
    >>> count_vowels_frozenset("aeiouAEIOU")
    10
    """
    return sum(1 for char in s if char in _VOWELS)


def count_vowels_translate(s: str) -> int:
    """
    Count vowels by deleting all non-vowels with str.translate (C-level),
    then taking the length. Fastest for ASCII strings.

    Note: only handles ASCII — non-ASCII characters are left in place,
    so Unicode text with accented vowels (é, ü, etc.) may over-count.

    >>> count_vowels_translate("hello world")
    3
    >>> count_vowels_translate("HELLO WORLD")
    3
    >>> count_vowels_translate("")
    0
    >>> count_vowels_translate("PYTHON")
    1
    >>> count_vowels_translate("aeiouAEIOU")
    10
    """
    return len(s.translate(_DELETE_NON_VOWELS))


def benchmark() -> None:
    from timeit import timeit
    from count_vowels import count_vowels

    n = 500_000
    cases = [
        ("short",  "hello world"),
        ("medium", "the quick brown fox jumps over the lazy dog"),
        ("long",   "the quick brown fox jumps over the lazy dog" * 10),
    ]

    print(f"Benchmarking {n:,} runs:\n")
    for label, msg in cases:
        t_orig = timeit(
            "count_vowels(msg)",
            setup=f"from count_vowels import count_vowels; msg={msg!r}",
            number=n,
        )
        t_fs = timeit(
            "count_vowels_frozenset(msg)",
            setup=f"from count_vowels_optimized import count_vowels_frozenset; msg={msg!r}",
            number=n,
        )
        t_tr = timeit(
            "count_vowels_translate(msg)",
            setup=f"from count_vowels_optimized import count_vowels_translate; msg={msg!r}",
            number=n,
        )

        print(f"  {label} ({len(msg)} chars):")
        print(f"    original  (generator + str membership) {t_orig:.4f}s")
        print(f"    frozenset (generator + hash lookup)     {t_fs:.4f}s")
        print(f"    translate (C-level delete + len)        {t_tr:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
