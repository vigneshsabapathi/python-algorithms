"""
Optimized implementations for checking if a string contains only unique characters.
Companion to is_contains_unique_chars.py — see that file for the pow()-based bitmask baseline.
"""


def is_unique_set(input_str: str) -> bool:
    """
    O(n) set-size comparison — simplest and most readable.
    A duplicate character makes the set smaller than the string.

    >>> is_unique_set("I_love.py")
    True
    >>> is_unique_set("I don't love Python")
    False
    >>> is_unique_set("")
    True
    >>> is_unique_set("a")
    True
    """
    return len(input_str) == len(set(input_str))


def is_unique_early_exit(input_str: str) -> bool:
    """
    O(n) with early exit — returns False as soon as the first duplicate is found.
    Best for strings that repeat early; worst case same as set approach.

    >>> is_unique_early_exit("I_love.py")
    True
    >>> is_unique_early_exit("I don't love Python")
    False
    >>> is_unique_early_exit("")
    True
    >>> is_unique_early_exit("a")
    True
    """
    seen = set()
    for ch in input_str:
        if ch in seen:
            return False
        seen.add(ch)
    return True


def is_unique_bitmask_fast(input_str: str) -> bool:
    """
    Bitmask approach using left-shift (1 << n) instead of pow(2, n).
    Functionally identical to the original but avoids the slow pow() call.

    >>> is_unique_bitmask_fast("I_love.py")
    True
    >>> is_unique_bitmask_fast("I don't love Python")
    False
    >>> is_unique_bitmask_fast("")
    True
    >>> is_unique_bitmask_fast("a")
    True
    """
    bitmap = 0
    for ch in input_str:
        ch_unicode = ord(ch)
        if bitmap >> ch_unicode & 1:
            return False
        bitmap |= 1 << ch_unicode  # << is a C-level op; pow() is Python-level
    return True


def benchmark() -> None:
    """Benchmark all four unique-char implementations."""
    from timeit import timeit

    n = 100_000
    test_str = "I_love.py"   # 9-char unique string — full scan

    cases = [
        ('is_contains_unique_chars("I_love.py")',  "from is_contains_unique_chars import is_contains_unique_chars",   "pow() bitmask   (original)"),
        ('is_unique_bitmask_fast("I_love.py")',    "from is_contains_unique_chars_optimized import is_unique_bitmask_fast", "shift bitmask   (optimized)"),
        ('is_unique_set("I_love.py")',              "from is_contains_unique_chars_optimized import is_unique_set",    "set compare     (optimized)"),
        ('is_unique_early_exit("I_love.py")',       "from is_contains_unique_chars_optimized import is_unique_early_exit", "early exit set  (optimized)"),
    ]

    print(f"Benchmarking {n:,} runs on '{test_str}':\n")
    for stmt, setup, label in cases:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {label:<30} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
