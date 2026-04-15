"""
Decimal to Binary - Optimized Variants with Benchmarks
"""

import timeit


def dec_to_bin_loop(decimal: int) -> str:
    """
    Division-remainder loop.

    >>> dec_to_bin_loop(255)
    '0b11111111'
    """
    if decimal == 0:
        return "0b0"
    neg = decimal < 0
    decimal = abs(decimal)
    bits = []
    while decimal > 0:
        bits.append(str(decimal & 1))
        decimal >>= 1
    result = "0b" + "".join(reversed(bits))
    return "-" + result if neg else result


def dec_to_bin_builtin(decimal: int) -> str:
    """
    Python built-in bin().

    >>> dec_to_bin_builtin(255)
    '0b11111111'
    """
    return bin(decimal)


def dec_to_bin_format(decimal: int) -> str:
    """
    Format string approach.

    >>> dec_to_bin_format(255)
    '0b11111111'
    """
    if decimal < 0:
        return "-0b" + f"{abs(decimal):b}"
    return "0b" + f"{decimal:b}"


def dec_to_bin_recursive(decimal: int) -> str:
    """
    Recursive approach.

    >>> dec_to_bin_recursive(255)
    '0b11111111'
    """
    if decimal < 0:
        return "-" + dec_to_bin_recursive(-decimal)
    if decimal == 0:
        return "0b0"

    def _recurse(n):
        if n == 0:
            return ""
        return _recurse(n >> 1) + str(n & 1)

    return "0b" + _recurse(decimal)


def benchmark():
    test_input = 2**32 - 1
    number = 100_000
    print(f"Benchmark: converting {test_input} ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", dec_to_bin_loop), ("Built-in", dec_to_bin_builtin),
                         ("Format", dec_to_bin_format), ("Recursive", dec_to_bin_recursive)]:
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
