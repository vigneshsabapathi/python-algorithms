"""
Decimal to Any Base - Optimized Variants with Benchmarks
"""

import timeit

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def dec_to_any_loop(num: int, base: int) -> str:
    """
    Standard division loop.

    >>> dec_to_any_loop(255, 16)
    'FF'
    """
    if num == 0:
        return "0"
    result = []
    while num > 0:
        result.append(DIGITS[num % base])
        num //= base
    return "".join(reversed(result))


def dec_to_any_recursive(num: int, base: int) -> str:
    """
    Recursive approach.

    >>> dec_to_any_recursive(255, 16)
    'FF'
    """
    if num < base:
        return DIGITS[num]
    return dec_to_any_recursive(num // base, base) + DIGITS[num % base]


def dec_to_any_divmod(num: int, base: int) -> str:
    """
    Using divmod for single operation.

    >>> dec_to_any_divmod(255, 16)
    'FF'
    """
    if num == 0:
        return "0"
    result = []
    while num > 0:
        num, remainder = divmod(num, base)
        result.append(DIGITS[remainder])
    return "".join(reversed(result))


def benchmark():
    test_input = 2**32 - 1
    number = 100_000
    print(f"Benchmark: converting {test_input} to base 16 ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", dec_to_any_loop), ("Recursive", dec_to_any_recursive),
                         ("Divmod", dec_to_any_divmod)]:
        t = timeit.timeit(lambda: func(test_input, 16), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
