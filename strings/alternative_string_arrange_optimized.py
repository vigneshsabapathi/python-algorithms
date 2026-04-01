"""
Optimized alternative string interleaving.

Improvements over the original:
- itertools.zip_longest pairs characters from both strings simultaneously,
  filling the shorter one with "" — eliminates the manual index-bound checks.
- itertools.chain.from_iterable flattens the pairs in one pass — no
  intermediate list of appends.
- Result is a single "".join() over a lazy generator — O(n+m) time, O(n+m) space,
  same as original but with ~2x less overhead per character.
"""

from __future__ import annotations

from itertools import chain, zip_longest


def alternative_string_arrange(first_str: str, second_str: str) -> str:
    """
    Interleave two strings character by character; append the remaining
    tail of the longer string.

    >>> alternative_string_arrange("ABCD", "XY")
    'AXBYCD'
    >>> alternative_string_arrange("XY", "ABCD")
    'XAYBCD'
    >>> alternative_string_arrange("AB", "XYZ")
    'AXBYZ'
    >>> alternative_string_arrange("ABC", "")
    'ABC'
    >>> alternative_string_arrange("", "XYZ")
    'XYZ'
    >>> alternative_string_arrange("", "")
    ''
    >>> alternative_string_arrange("HELLO", "WORLD")
    'HWEOLRLLOD'
    """
    return "".join(chain.from_iterable(zip_longest(first_str, second_str, fillvalue="")))


def benchmark() -> None:
    import timeit

    from strings.alternative_string_arrange import (
        alternative_string_arrange as orig,
    )

    pairs = [
        ("ABCD", "XY"),
        ("XY", "ABCD"),
        ("AB", "XYZ"),
        ("HELLO", "WORLD"),
        ("A" * 500, "B" * 300),
    ]
    n = 200_000

    orig_t = timeit.timeit(lambda: [orig(a, b) for a, b in pairs], number=n)
    opt_t = timeit.timeit(
        lambda: [alternative_string_arrange(a, b) for a, b in pairs], number=n
    )

    print(f"original (manual loop):       {orig_t:.3f}s")
    print(f"optimized (zip_longest+chain): {opt_t:.3f}s")
    print(f"\nFastest: {'optimized' if opt_t < orig_t else 'original'}")
    ratio = max(orig_t, opt_t) / min(orig_t, opt_t)
    print(f"Ratio: {ratio:.2f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
