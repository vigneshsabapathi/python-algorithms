"""
Octal to Binary - Optimized Variants with Benchmarks
"""

import timeit


def oct_to_bin_lookup(octal_string: str) -> str:
    """
    3-bit lookup table per octal digit.

    >>> oct_to_bin_lookup("377")
    '0b11111111'
    """
    o2b = {str(i): f"{i:03b}" for i in range(8)}
    binary = "".join(o2b[c] for c in octal_string).lstrip("0") or "0"
    return "0b" + binary


def oct_to_bin_builtin(octal_string: str) -> str:
    """
    Python built-in int() then bin().

    >>> oct_to_bin_builtin("377")
    '0b11111111'
    """
    return bin(int(octal_string, 8))


def oct_to_bin_bitwise(octal_string: str) -> str:
    """
    Convert digit by digit with bit shifting.

    >>> oct_to_bin_bitwise("377")
    '0b11111111'
    """
    num = 0
    for c in octal_string:
        num = (num << 3) | int(c)
    return bin(num)


def benchmark():
    test_input = "7" * 10
    number = 100_000
    print(f"Benchmark: converting '{test_input}' ({number:,} iterations)\n")
    results = []
    for label, func in [("Lookup", oct_to_bin_lookup), ("Built-in", oct_to_bin_builtin),
                         ("Bitwise", oct_to_bin_bitwise)]:
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
