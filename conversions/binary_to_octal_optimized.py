"""
Binary to Octal - Optimized Variants with Benchmarks
"""

import timeit


def bin_to_oct_groups(binary_string: str) -> str:
    """
    Group 3 bits at a time with lookup.

    >>> bin_to_oct_groups("1111")
    '0o17'
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    padded = binary_string.zfill((len(binary_string) + 2) // 3 * 3)
    digits = [str(int(padded[i:i+3], 2)) for i in range(0, len(padded), 3)]
    return "0o" + ("".join(digits).lstrip("0") or "0")


def bin_to_oct_builtin(binary_string: str) -> str:
    """
    Python built-in int() then oct().

    >>> bin_to_oct_builtin("1111")
    '0o17'
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    return oct(int(binary_string, 2))


def bin_to_oct_bitwise(binary_string: str) -> str:
    """
    Bitwise extraction of 3-bit groups.

    >>> bin_to_oct_bitwise("1111")
    '0o17'
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    num = int(binary_string, 2)
    if num == 0:
        return "0o0"
    digits = []
    while num > 0:
        digits.append(str(num & 7))
        num >>= 3
    return "0o" + "".join(reversed(digits))


def benchmark():
    test_input = "1" * 32
    number = 100_000
    print(f"Benchmark: converting '{test_input[:16]}...' ({number:,} iterations)\n")
    results = []
    for label, func in [("Group-3", bin_to_oct_groups),
                         ("Built-in", bin_to_oct_builtin),
                         ("Bitwise", bin_to_oct_bitwise)]:
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
