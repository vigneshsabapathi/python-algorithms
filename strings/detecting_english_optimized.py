"""
Optimized English detection.
Companion to detecting_english_programmatically.py.

Key improvements:
  1. Load dictionary into a frozenset (hash lookup O(1), immutable)
  2. Use str.translate for non-letter removal (C-level, vs generator per char)
  3. Use sum() + generator instead of list comprehension for word match count
"""

import os
from string import ascii_letters

# Build a delete table that removes every char NOT in letters/space
_KEEP = set(ascii_letters + " \t\n")
_ALL_CHARS = {chr(i) for i in range(128)}
_DELETE_TABLE = str.maketrans("", "", "".join(_ALL_CHARS - _KEEP))


def _load_dictionary() -> frozenset[str]:
    path = os.path.dirname(os.path.realpath(__file__))
    with open(path + "/dictionary.txt") as f:
        return frozenset(f.read().split("\n"))


ENGLISH_WORDS: frozenset[str] = _load_dictionary()


def remove_non_letters_fast(message: str) -> str:
    """
    Removes non-letter, non-space characters using str.translate (C-level).
    Faster than the generator-per-char approach for longer strings.

    >>> remove_non_letters_fast("Hi! how are you?")
    'Hi how are you'
    >>> remove_non_letters_fast("P^y%t)h@o*n")
    'Python'
    >>> remove_non_letters_fast("1+1=2")
    ''
    >>> remove_non_letters_fast("www.google.com/")
    'wwwgooglecom'
    >>> remove_non_letters_fast("")
    ''
    """
    return message.translate(_DELETE_TABLE)


def get_english_count_fast(message: str) -> float:
    cleaned = remove_non_letters_fast(message.upper())
    possible_words = cleaned.split()
    if not possible_words:
        return 0.0
    # sum() + generator avoids building an intermediate list
    matches = sum(1 for word in possible_words if word in ENGLISH_WORDS)
    return matches / len(possible_words)


def is_english_fast(
    message: str, word_percentage: int = 20, letter_percentage: int = 85
) -> bool:
    """
    >>> is_english_fast('Hello World')
    True
    >>> is_english_fast('llold HorWd')
    False
    """
    if not message:
        return False
    words_match = get_english_count_fast(message) * 100 >= word_percentage
    num_letters = len(remove_non_letters_fast(message))
    letters_match = (num_letters / len(message)) * 100 >= letter_percentage
    return words_match and letters_match


def benchmark() -> None:
    from timeit import timeit

    n = 20_000
    msg = "The quick brown fox jumps over the lazy dog"

    cases = [
        ('get_english_count(msg)',
         "from detecting_english_programmatically import get_english_count; "
         "msg='The quick brown fox jumps over the lazy dog'",
         "original  (list comp + set dict)"),
        ('get_english_count_fast(msg)',
         "from detecting_english_optimized import get_english_count_fast; "
         "msg='The quick brown fox jumps over the lazy dog'",
         "optimized (translate + frozenset)"),
    ]

    print(f"Benchmarking {n:,} runs on a {len(msg)}-char sentence:\n")
    for stmt, setup, label in cases:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {label:<38} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
