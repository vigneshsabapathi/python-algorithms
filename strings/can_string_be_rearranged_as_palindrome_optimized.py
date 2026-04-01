"""
Optimized palindrome-rearrangement checks.
Companion to can_string_be_rearranged_as_palindrome.py.

Four approaches compared:
  1. Counter + sum       — original counter variant
  2. dict.get + count    — original manual dict variant
  3. Set toggle          — no frequency dict; toggle membership on each char
  4. Bitmask (a-z only)  — XOR one bit per char; popcount at end; O(1) space

Key insight: A string can be rearranged into a palindrome iff at most ONE
character has an odd frequency. The set-toggle approach tracks exactly this
without ever storing counts — add on first sight, remove on second, etc.
"""

from collections import Counter


def _clean(s: str) -> str:
    return s.replace(" ", "").lower()


# ---------------------------------------------------------------------------
# 1. Set toggle — no frequency dict needed ✅ Recommended
# ---------------------------------------------------------------------------

def can_palindrome_set(input_str: str = "") -> bool:
    """
    Toggle a set: add char if not present (odd count so far), remove if present
    (even count so far). At the end, len(odd_chars) <= 1 means palindrome-ready.

    Works for any character (not just a-z). O(n) time, O(k) space.

    >>> can_palindrome_set("Momo")
    True
    >>> can_palindrome_set("Mother")
    False
    >>> can_palindrome_set("A man a plan a canal Panama")
    True
    >>> can_palindrome_set("")
    True
    >>> can_palindrome_set("a")
    True
    >>> can_palindrome_set("ab")
    False
    """
    odd_chars: set[str] = set()
    for c in _clean(input_str):
        # Toggle: remove if already seen an odd number of times (now even), add otherwise.
        # Avoids building a frequency dict — tracks only parity, not count.
        if c in odd_chars:
            odd_chars.discard(c)
        else:
            odd_chars.add(c)
    return len(odd_chars) <= 1


# ---------------------------------------------------------------------------
# 2. Bitmask — O(1) space, a-z only
# ---------------------------------------------------------------------------

def can_palindrome_bitmask(input_str: str = "") -> bool:
    """
    XOR one bit per character (bit position = ord(c) - ord('a')).
    If the result has at most 1 set bit, the string can form a palindrome.

    Restriction: only handles lowercase a-z (digits/punctuation are ignored
    via the isalpha() guard). Use can_palindrome_set for arbitrary input.

    >>> can_palindrome_bitmask("Momo")
    True
    >>> can_palindrome_bitmask("Mother")
    False
    >>> can_palindrome_bitmask("A man a plan a canal Panama")
    True
    >>> can_palindrome_bitmask("")
    True
    >>> can_palindrome_bitmask("a")
    True
    >>> can_palindrome_bitmask("ab")
    False
    """
    mask = 0
    for c in _clean(input_str):
        if c.isalpha():
            mask ^= 1 << (ord(c) - ord("a"))
    # At most one bit set: mask & (mask - 1) clears the lowest set bit.
    # If result is 0, there was at most one set bit.
    return mask == 0 or (mask & (mask - 1)) == 0


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    from timeit import timeit

    n = 300_000
    cases = [
        ("short",  "Momo"),
        ("medium", "A man a plan a canal Panama"),
        ("long",   "A man a plan a canal Panama" * 10),
    ]

    print(f"Benchmarking {n:,} runs:\n")
    for label, msg in cases:
        t_ctr = timeit(
            "can_string_be_rearranged_as_palindrome_counter(s)",
            setup=(
                "from can_string_be_rearranged_as_palindrome import "
                "can_string_be_rearranged_as_palindrome_counter; "
                f"s={msg!r}"
            ),
            number=n,
        )
        t_dct = timeit(
            "can_string_be_rearranged_as_palindrome(s)",
            setup=(
                "from can_string_be_rearranged_as_palindrome import "
                "can_string_be_rearranged_as_palindrome; "
                f"s={msg!r}"
            ),
            number=n,
        )
        t_set = timeit(
            "can_palindrome_set(s)",
            setup=(
                "from can_string_be_rearranged_as_palindrome_optimized import "
                f"can_palindrome_set; s={msg!r}"
            ),
            number=n,
        )
        t_bit = timeit(
            "can_palindrome_bitmask(s)",
            setup=(
                "from can_string_be_rearranged_as_palindrome_optimized import "
                f"can_palindrome_bitmask; s={msg!r}"
            ),
            number=n,
        )

        print(f"  {label} ({len(msg)} chars):")
        print(f"    Counter + sum   (original counter)   {t_ctr:.4f}s")
        print(f"    dict.get + loop (original dict)       {t_dct:.4f}s")
        print(f"    set toggle      (no freq dict)        {t_set:.4f}s")
        print(f"    bitmask         (a-z only, O(1) space) {t_bit:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
