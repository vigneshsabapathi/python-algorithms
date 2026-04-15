"""
Hexadecimal to Decimal - Optimized Variants with Benchmarks
"""

import timeit


def hex_to_dec_loop(hex_string: str) -> int:
    """
    Manual Horner's method loop.

    >>> hex_to_dec_loop("FF")
    255
    """
    hex_map = {c: i for i, c in enumerate("0123456789ABCDEF")}
    result = 0
    for char in hex_string.upper():
        result = result * 16 + hex_map[char]
    return result


def hex_to_dec_builtin(hex_string: str) -> int:
    """
    Python built-in int() with base 16.

    >>> hex_to_dec_builtin("FF")
    255
    """
    return int(hex_string, 16)


def hex_to_dec_enumerate(hex_string: str) -> int:
    """
    Enumerate from right with powers.

    >>> hex_to_dec_enumerate("FF")
    255
    """
    hex_map = {c: i for i, c in enumerate("0123456789ABCDEF")}
    return sum(hex_map[c] * (16 ** i) for i, c in enumerate(reversed(hex_string.upper())))


def benchmark():
    test_input = "FFFFFFFF"
    number = 100_000
    print(f"Benchmark: converting '{test_input}' ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", hex_to_dec_loop), ("Built-in", hex_to_dec_builtin),
                         ("Enumerate", hex_to_dec_enumerate)]:
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
