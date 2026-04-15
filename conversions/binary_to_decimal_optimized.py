"""
Binary to Decimal Conversion - Optimized Variants with Benchmarks

Three+ approaches compared for converting binary strings to decimal integers.
"""

import timeit


def binary_to_decimal_loop(binary_string: str) -> int:
    """
    Manual loop with multiply-and-add (Horner's method).

    >>> binary_to_decimal_loop("101")
    5
    >>> binary_to_decimal_loop("1111")
    15
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    decimal = 0
    for char in binary_string:
        decimal = decimal * 2 + int(char)
    return decimal


def binary_to_decimal_builtin(binary_string: str) -> int:
    """
    Python built-in int() with base 2.

    >>> binary_to_decimal_builtin("101")
    5
    >>> binary_to_decimal_builtin("1111")
    15
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    return int(binary_string, 2)


def binary_to_decimal_bitshift(binary_string: str) -> int:
    """
    Bit-shift approach: shift left and OR each bit.

    >>> binary_to_decimal_bitshift("101")
    5
    >>> binary_to_decimal_bitshift("1111")
    15
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    result = 0
    for char in binary_string:
        result = (result << 1) | (char == "1")
    return result


def binary_to_decimal_enumerate(binary_string: str) -> int:
    """
    Enumerate powers from right to left using enumerate.

    >>> binary_to_decimal_enumerate("101")
    5
    >>> binary_to_decimal_enumerate("1111")
    15
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    return sum(int(bit) << i for i, bit in enumerate(reversed(binary_string)))


def benchmark():
    test_input = "1" * 32  # 32-bit all ones
    number = 100_000

    variants = [
        ("Loop (Horner)", "binary_to_decimal_loop"),
        ("Built-in int()", "binary_to_decimal_builtin"),
        ("Bit-shift", "binary_to_decimal_bitshift"),
        ("Enumerate", "binary_to_decimal_enumerate"),
    ]

    print(f"Benchmark: converting '{test_input}' ({number:,} iterations)\n")
    results = []
    for label, func_name in variants:
        t = timeit.timeit(
            f"{func_name}('{test_input}')",
            globals=globals(),
            number=number,
        )
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<22} {ms:.4f} ms/call")

    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
