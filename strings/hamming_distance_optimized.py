"""
Optimized Hamming distance implementations.
Companion to hamming_distance.py — see that file for the loop-based baseline.

Hamming distance: number of positions where two equal-length strings differ.
https://en.wikipedia.org/wiki/Hamming_distance
"""


def hamming_distance_sum(string1: str, string2: str) -> int:
    """
    O(n) using sum() over a generator expression.
    sum() is a C-level accumulator — faster than a Python for loop.

    >>> hamming_distance_sum("python", "python")
    0
    >>> hamming_distance_sum("karolin", "kathrin")
    3
    >>> hamming_distance_sum("00000", "11111")
    5
    >>> hamming_distance_sum("karolin", "kath")
    Traceback (most recent call last):
      ...
    ValueError: String lengths must match!
    """
    if len(string1) != len(string2):
        raise ValueError("String lengths must match!")
    return sum(c1 != c2 for c1, c2 in zip(string1, string2))


def hamming_distance_map(string1: str, string2: str) -> int:
    """
    O(n) using map(str.__ne__, ...) — runs almost entirely at C level.
    map() applies str.__ne__ pairwise without a Python loop body.

    >>> hamming_distance_map("python", "python")
    0
    >>> hamming_distance_map("karolin", "kathrin")
    3
    >>> hamming_distance_map("00000", "11111")
    5
    >>> hamming_distance_map("karolin", "kath")
    Traceback (most recent call last):
      ...
    ValueError: String lengths must match!
    """
    if len(string1) != len(string2):
        raise ValueError("String lengths must match!")
    return sum(map(str.__ne__, string1, string2))


def benchmark() -> None:
    """Benchmark all three Hamming distance implementations."""
    from timeit import timeit

    n = 200_000
    s1 = "karolin"
    s2 = "kathrin"

    cases = [
        (f'hamming_distance("{s1}", "{s2}")',
         "from hamming_distance import hamming_distance",
         "loop + count    (original)"),
        (f'hamming_distance_sum("{s1}", "{s2}")',
         "from hamming_distance_optimized import hamming_distance_sum",
         "sum + generator (optimized)"),
        (f'hamming_distance_map("{s1}", "{s2}")',
         "from hamming_distance_optimized import hamming_distance_map",
         "map + str.__ne__ (optimized)"),
    ]

    print(f"Benchmarking {n:,} runs on ('{s1}', '{s2}'):\n")
    for stmt, setup, label in cases:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {label:<30} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
