"""
Optimized anagram finder.

Improvements over the original:
- Sorted-string signature: "".join(sorted(word)) replaces Counter + format string.
  Simpler, and faster for typical word lengths (< ~15 chars).
- Tuple signature variant: tuple(sorted(word)) skips the join entirely —
  tuples are valid dict keys and avoid string allocation.
- Both approaches benchmarked against the original Counter-based signature.
"""

from __future__ import annotations

import collections
from pathlib import Path


# --- Signature strategies ---

def signature_sorted_str(word: str) -> str:
    """
    Sorted-character string signature.

    >>> signature_sorted_str("test")
    'estt'
    >>> signature_sorted_str("listen")
    'eilnst'
    >>> signature_sorted_str("silent")
    'eilnst'
    >>> signature_sorted_str("")
    ''
    """
    return "".join(sorted(word))


def signature_sorted_tuple(word: str) -> tuple[str, ...]:
    """
    Sorted-character tuple signature — skips the join, usable as dict key.

    >>> signature_sorted_tuple("test")
    ('e', 's', 't', 't')
    >>> signature_sorted_tuple("listen") == signature_sorted_tuple("silent")
    True
    """
    return tuple(sorted(word))


# --- Build lookup tables ---

data: str = Path(__file__).parent.joinpath("words.txt").read_text(encoding="utf-8")
word_list = sorted({word.strip().lower() for word in data.splitlines()})

# Sorted-string variant
_by_sorted_str: dict[str, list[str]] = collections.defaultdict(list)
for _word in word_list:
    _by_sorted_str[signature_sorted_str(_word)].append(_word)

# Sorted-tuple variant
_by_sorted_tuple: dict[tuple, list[str]] = collections.defaultdict(list)
for _word in word_list:
    _by_sorted_tuple[signature_sorted_tuple(_word)].append(_word)


def anagram_sorted_str(my_word: str) -> list[str]:
    """
    Return every dictionary anagram using the sorted-string key.

    >>> anagram_sorted_str('test')
    ['sett', 'stet', 'test']
    >>> anagram_sorted_str('listen')
    ['enlist', 'listen', 'silent', 'tinsel']
    >>> anagram_sorted_str('this is a test')
    []
    >>> anagram_sorted_str('final')
    ['final']
    """
    return _by_sorted_str[signature_sorted_str(my_word)]


def anagram_sorted_tuple(my_word: str) -> list[str]:
    """
    Return every dictionary anagram using the sorted-tuple key.

    >>> anagram_sorted_tuple('test')
    ['sett', 'stet', 'test']
    >>> anagram_sorted_tuple('listen')
    ['enlist', 'listen', 'silent', 'tinsel']
    >>> anagram_sorted_tuple('final')
    ['final']
    """
    return _by_sorted_tuple[signature_sorted_tuple(my_word)]


def benchmark() -> None:
    import timeit

    from strings.anagrams import signature as orig_signature, anagram as orig_anagram

    words_sample = ["test", "listen", "silent", "eat", "dog", "final"]
    n = 200_000

    orig_sig = timeit.timeit(
        lambda: [orig_signature(w) for w in words_sample], number=n
    )
    opt_str_sig = timeit.timeit(
        lambda: [signature_sorted_str(w) for w in words_sample], number=n
    )
    opt_tup_sig = timeit.timeit(
        lambda: [signature_sorted_tuple(w) for w in words_sample], number=n
    )

    orig_lookup = timeit.timeit(lambda: [orig_anagram(w) for w in words_sample], number=n)
    opt_str_lookup = timeit.timeit(lambda: [anagram_sorted_str(w) for w in words_sample], number=n)
    opt_tup_lookup = timeit.timeit(lambda: [anagram_sorted_tuple(w) for w in words_sample], number=n)

    print(f"signature (6 words, {n} iters):")
    print(f"  original (Counter + format):  {orig_sig:.3f}s")
    print(f"  optimized (sorted str join):  {opt_str_sig:.3f}s")
    print(f"  optimized (sorted tuple):     {opt_tup_sig:.3f}s")
    print()
    print(f"anagram lookup (6 words, {n} iters):")
    print(f"  original:                     {orig_lookup:.3f}s")
    print(f"  optimized (sorted str):       {opt_str_lookup:.3f}s")
    print(f"  optimized (sorted tuple):     {opt_tup_lookup:.3f}s")

    sigs = [orig_sig, opt_str_sig, opt_tup_sig]
    names = ["original", "sorted-str", "sorted-tuple"]
    print(f"\nFastest signature: {names[sigs.index(min(sigs))]}")
    lkps = [orig_lookup, opt_str_lookup, opt_tup_lookup]
    print(f"Fastest lookup:    {names[lkps.index(min(lkps))]}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
