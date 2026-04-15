"""
Excel Title to Column - Optimized Variants with Benchmarks
"""

import timeit


def excel_title_loop(title: str) -> int:
    """
    Standard loop: treat as base-26 number.

    >>> excel_title_loop("ZY")
    701
    """
    result = 0
    for c in title.upper():
        result = result * 26 + (ord(c) - 64)
    return result


def excel_title_reduce(title: str) -> int:
    """
    Functional reduce approach.

    >>> excel_title_reduce("ZY")
    701
    """
    from functools import reduce
    return reduce(lambda acc, c: acc * 26 + (ord(c) - 64), title.upper(), 0)


def excel_title_enumerate(title: str) -> int:
    """
    Enumerate from right with powers of 26.

    >>> excel_title_enumerate("ZY")
    701
    """
    return sum((ord(c) - 64) * (26 ** i) for i, c in enumerate(reversed(title.upper())))


def benchmark():
    test_input = "ZZZ"
    number = 100_000
    print(f"Benchmark: converting '{test_input}' ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", excel_title_loop), ("Reduce", excel_title_reduce),
                         ("Enumerate", excel_title_enumerate)]:
        t = timeit.timeit(lambda: func(test_input), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
