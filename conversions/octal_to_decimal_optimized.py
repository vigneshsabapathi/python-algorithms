"""
Octal to Decimal - Optimized Variants with Benchmarks
"""

import timeit


def oct_to_dec_loop(octal: int) -> int:
    """
    Extract digits and multiply by powers of 8.

    >>> oct_to_dec_loop(377)
    255
    """
    decimal = 0
    place = 0
    while octal > 0:
        decimal += (octal % 10) * (8 ** place)
        octal //= 10
        place += 1
    return decimal


def oct_to_dec_builtin(octal: int) -> int:
    """
    Convert to string and use int() with base 8.

    >>> oct_to_dec_builtin(377)
    255
    """
    return int(str(octal), 8)


def oct_to_dec_horner(octal: int) -> int:
    """
    Horner's method: process digits left to right.

    >>> oct_to_dec_horner(377)
    255
    """
    digits = str(octal)
    result = 0
    for d in digits:
        result = result * 8 + int(d)
    return result


def benchmark():
    test_input = 7777777777
    number = 100_000
    print(f"Benchmark: converting {test_input} ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", oct_to_dec_loop), ("Built-in", oct_to_dec_builtin),
                         ("Horner", oct_to_dec_horner)]:
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
