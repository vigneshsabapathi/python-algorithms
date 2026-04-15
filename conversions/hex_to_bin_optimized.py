"""
Hex to Binary - Optimized Variants with Benchmarks
"""

import timeit


def hex_to_bin_lookup(hex_string: str) -> str:
    """
    4-bit lookup table per hex digit.

    >>> hex_to_bin_lookup("FF")
    '11111111'
    """
    h2b = {c: f"{i:04b}" for i, c in enumerate("0123456789ABCDEF")}
    binary = "".join(h2b[c] for c in hex_string.upper())
    return binary.lstrip("0") or "0"


def hex_to_bin_builtin(hex_string: str) -> str:
    """
    Python built-in int() then bin().

    >>> hex_to_bin_builtin("FF")
    '11111111'
    """
    return bin(int(hex_string, 16))[2:]


def hex_to_bin_format(hex_string: str) -> str:
    """
    Format string approach.

    >>> hex_to_bin_format("FF")
    '11111111'
    """
    return f"{int(hex_string, 16):b}"


def benchmark():
    test_input = "DEADBEEF"
    number = 100_000
    print(f"Benchmark: converting '{test_input}' ({number:,} iterations)\n")
    results = []
    for label, func in [("Lookup", hex_to_bin_lookup), ("Built-in", hex_to_bin_builtin),
                         ("Format", hex_to_bin_format)]:
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
