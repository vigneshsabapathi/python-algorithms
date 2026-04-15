"""
Decimal to Hexadecimal - Optimized Variants with Benchmarks
"""

import timeit

HEX_DIGITS = "0123456789ABCDEF"


def dec_to_hex_loop(decimal: int) -> str:
    """
    Division-remainder loop.

    >>> dec_to_hex_loop(255)
    '0xFF'
    """
    if decimal == 0:
        return "0x0"
    neg = decimal < 0
    decimal = abs(decimal)
    digits = []
    while decimal > 0:
        digits.append(HEX_DIGITS[decimal & 15])
        decimal >>= 4
    result = "0x" + "".join(reversed(digits))
    return "-" + result if neg else result


def dec_to_hex_builtin(decimal: int) -> str:
    """
    Python built-in hex().

    >>> dec_to_hex_builtin(255)
    '0xFF'
    """
    if decimal < 0:
        return "-0x" + hex(abs(decimal))[2:].upper()
    return "0x" + hex(decimal)[2:].upper()


def dec_to_hex_format(decimal: int) -> str:
    """
    Format string approach.

    >>> dec_to_hex_format(255)
    '0xFF'
    """
    if decimal < 0:
        return "-0x" + f"{abs(decimal):X}"
    return "0x" + f"{decimal:X}"


def benchmark():
    test_input = 2**32 - 1
    number = 100_000
    print(f"Benchmark: converting {test_input} ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", dec_to_hex_loop), ("Built-in", dec_to_hex_builtin),
                         ("Format", dec_to_hex_format)]:
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
