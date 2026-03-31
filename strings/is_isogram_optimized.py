"""
Optimized isogram implementations.
Companion to is_isogram.py — see that file for the sort-based baseline.

wiki: https://en.wikipedia.org/wiki/Heterogram_(literature)#Isograms
"""


def is_isogram_set(string: str) -> bool:
    """
    O(n) set-size comparison — no sorting needed.
    Lowercases once, builds a set of unique letters, compares size to original.

    >>> is_isogram_set('Uncopyrightable')
    True
    >>> is_isogram_set('allowance')
    False
    >>> is_isogram_set('Ambidextrously')
    True
    >>> is_isogram_set('copy1')
    Traceback (most recent call last):
     ...
    ValueError: String must only contain alphabetic characters.
    """
    if not all(x.isalpha() for x in string):
        raise ValueError("String must only contain alphabetic characters.")
    return len(string) == len(set(string.lower()))


def is_isogram_early_exit(string: str) -> bool:
    """
    O(n) with early exit — stops as soon as the first repeated letter is found.
    Best case O(1) for strings that repeat immediately (e.g. "aa...").

    >>> is_isogram_early_exit('Uncopyrightable')
    True
    >>> is_isogram_early_exit('allowance')
    False
    >>> is_isogram_early_exit('Ambidextrously')
    True
    >>> is_isogram_early_exit('copy1')
    Traceback (most recent call last):
     ...
    ValueError: String must only contain alphabetic characters.
    """
    if not all(x.isalpha() for x in string):
        raise ValueError("String must only contain alphabetic characters.")
    seen = set()
    for char in string.lower():
        if char in seen:
            return False
        seen.add(char)
    return True


def benchmark() -> None:
    """Benchmark all three isogram implementations."""
    from timeit import timeit

    setup = (
        "from __main__ import is_isogram_set, is_isogram_early_exit\n"
        "import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('.'))))\n"
        "from is_isogram import is_isogram"
    )

    word = "Uncopyrightable"   # 15-char isogram — full scan always needed

    # Run benchmarks using globals() to avoid module path issues
    n = 200_000
    t1 = timeit(f'is_isogram("{word}")', setup="from is_isogram import is_isogram", number=n)
    t2 = timeit(f'is_isogram_set("{word}")', setup="from is_isogram_optimized import is_isogram_set", number=n)
    t3 = timeit(f'is_isogram_early_exit("{word}")', setup="from is_isogram_optimized import is_isogram_early_exit", number=n)

    print(f"{'sort-based  (original)':<30} {n:>7,} runs in {t1:.4f}s")
    print(f"{'set compare (optimized)':<30} {n:>7,} runs in {t2:.4f}s")
    print(f"{'early exit  (optimized)':<30} {n:>7,} runs in {t3:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
