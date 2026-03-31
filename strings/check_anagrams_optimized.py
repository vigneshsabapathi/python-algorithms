"""
Optimized anagram checking implementations.
Companion to check_anagrams.py.

Three approaches compared:
  1. Original: defaultdict + Python loop          — O(n), but loop is Python-level
  2. Counter equality                             — O(n), C-level counting
  3. sorted equality                              — O(n log n), but entirely C

Key insight: collections.Counter is implemented in C and builds frequency maps
faster than a Python for-loop over a defaultdict. For short strings the overhead
of constructing two Counters is dominated by call setup; sorted() can win there.
For longer strings, Counter's O(n) C-level loop beats sorted's O(n log n).
"""

from collections import Counter


def _clean(s: str) -> str:
    """Lowercase and strip all spaces (shared by all variants)."""
    return s.lower().replace(" ", "")


def check_anagrams_counter(first_str: str, second_str: str) -> bool:
    """
    Anagram check using Counter equality — idiomatic Python.
    Counter(s1) == Counter(s2) compares frequency maps in C.

    >>> check_anagrams_counter('Silent', 'Listen')
    True
    >>> check_anagrams_counter('This is a string', 'Is this a string')
    True
    >>> check_anagrams_counter('There', 'Their')
    False
    >>> check_anagrams_counter('', '')
    True
    >>> check_anagrams_counter('abc', 'ab')
    False
    """
    return Counter(_clean(first_str)) == Counter(_clean(second_str))


def check_anagrams_sorted(first_str: str, second_str: str) -> bool:
    """
    Anagram check via sorted comparison — O(n log n) but runs entirely in C.
    Competitive with Counter for short strings.

    >>> check_anagrams_sorted('Silent', 'Listen')
    True
    >>> check_anagrams_sorted('This is a string', 'Is this a string')
    True
    >>> check_anagrams_sorted('There', 'Their')
    False
    >>> check_anagrams_sorted('', '')
    True
    >>> check_anagrams_sorted('abc', 'ab')
    False
    """
    s1, s2 = _clean(first_str), _clean(second_str)
    return sorted(s1) == sorted(s2)


def benchmark() -> None:
    from timeit import timeit

    n = 300_000
    cases = [
        ("short",  "Silent",         "Listen"),
        ("medium", "This is a string", "Is this a string"),
        ("long",   "the quick brown fox jumps over the lazy dog",
                   "over the lazy dog jumps the quick brown fox"),
    ]

    print(f"Benchmarking {n:,} runs:\n")
    for label, s1, s2 in cases:
        t_orig = timeit(
            "check_anagrams(s1, s2)",
            setup=f"from check_anagrams import check_anagrams; s1={s1!r}; s2={s2!r}",
            number=n,
        )
        t_ctr = timeit(
            "check_anagrams_counter(s1, s2)",
            setup=f"from check_anagrams_optimized import check_anagrams_counter; s1={s1!r}; s2={s2!r}",
            number=n,
        )
        t_srt = timeit(
            "check_anagrams_sorted(s1, s2)",
            setup=f"from check_anagrams_optimized import check_anagrams_sorted; s1={s1!r}; s2={s2!r}",
            number=n,
        )

        print(f"  {label} ({len(s1)!r} vs {len(s2)!r} chars):")
        print(f"    original  (defaultdict + Python loop) {t_orig:.4f}s")
        print(f"    Counter   (C-level frequency map)     {t_ctr:.4f}s")
        print(f"    sorted    (C-level sort comparison)   {t_srt:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
