"""
Octal to Hexadecimal - Optimized Variants with Benchmarks
"""

import timeit


def oct_to_hex_via_decimal(octal: int) -> str:
    """
    Two-step: octal -> decimal -> hex.

    >>> oct_to_hex_via_decimal(377)
    '0xFF'
    """
    decimal = int(str(octal), 8)
    return "0x" + f"{decimal:X}"


def oct_to_hex_via_binary(octal: int) -> str:
    """
    Two-step: octal -> binary -> hex (string manipulation).

    >>> oct_to_hex_via_binary(377)
    '0xFF'
    """
    o2b = {str(i): f"{i:03b}" for i in range(8)}
    binary = "".join(o2b[d] for d in str(octal))
    decimal = int(binary, 2)
    return "0x" + f"{decimal:X}" if decimal else "0x0"


def oct_to_hex_builtin(octal: int) -> str:
    """
    Python built-in chain.

    >>> oct_to_hex_builtin(377)
    '0xFF'
    """
    return "0x" + hex(int(str(octal), 8))[2:].upper()


def benchmark():
    test_input = 7777777777
    number = 100_000
    print(f"Benchmark: converting {test_input} ({number:,} iterations)\n")
    results = []
    for label, func in [("Via decimal", oct_to_hex_via_decimal),
                         ("Via binary", oct_to_hex_via_binary),
                         ("Built-in chain", oct_to_hex_builtin)]:
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
