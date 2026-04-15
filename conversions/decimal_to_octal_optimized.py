"""
Decimal to Octal - Optimized Variants with Benchmarks
"""

import timeit


def dec_to_oct_loop(decimal: int) -> int:
    """
    Division-remainder loop.

    >>> dec_to_oct_loop(255)
    377
    """
    if decimal == 0:
        return 0
    digits = []
    while decimal > 0:
        digits.append(str(decimal % 8))
        decimal //= 8
    return int("".join(reversed(digits)))


def dec_to_oct_builtin(decimal: int) -> int:
    """
    Python built-in oct(), converted to int.

    >>> dec_to_oct_builtin(255)
    377
    """
    return int(oct(decimal)[2:])


def dec_to_oct_bitwise(decimal: int) -> int:
    """
    Bitwise extraction of 3-bit groups.

    >>> dec_to_oct_bitwise(255)
    377
    """
    if decimal == 0:
        return 0
    digits = []
    while decimal > 0:
        digits.append(str(decimal & 7))
        decimal >>= 3
    return int("".join(reversed(digits)))


def benchmark():
    test_input = 2**20
    number = 100_000
    print(f"Benchmark: converting {test_input} ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", dec_to_oct_loop), ("Built-in", dec_to_oct_builtin),
                         ("Bitwise", dec_to_oct_bitwise)]:
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
