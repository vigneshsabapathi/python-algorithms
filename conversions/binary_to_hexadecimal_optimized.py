"""
Binary to Hexadecimal - Optimized Variants with Benchmarks
"""

import timeit


def bin_to_hex_lookup(binary_string: str) -> str:
    """
    Lookup table: group 4 bits at a time.

    >>> bin_to_hex_lookup("11001010")
    '0xCA'
    >>> bin_to_hex_lookup("1111")
    '0xF'
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    padded = binary_string.zfill((len(binary_string) + 3) // 4 * 4)
    hex_map = {f"{i:04b}": "0123456789ABCDEF"[i] for i in range(16)}
    digits = [hex_map[padded[i:i+4]] for i in range(0, len(padded), 4)]
    return "0x" + ("".join(digits).lstrip("0") or "0")


def bin_to_hex_builtin(binary_string: str) -> str:
    """
    Python built-in int() then hex().

    >>> bin_to_hex_builtin("11001010")
    '0xCA'
    >>> bin_to_hex_builtin("1111")
    '0xF'
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    return "0x" + hex(int(binary_string, 2))[2:].upper()


def bin_to_hex_format(binary_string: str) -> str:
    """
    Format string approach.

    >>> bin_to_hex_format("11001010")
    '0xCA'
    >>> bin_to_hex_format("1111")
    '0xF'
    """
    if not binary_string or not all(c in "01" for c in binary_string):
        raise ValueError("Invalid binary string")
    return "0x" + f"{int(binary_string, 2):X}"


def benchmark():
    test_input = "1" * 32
    number = 100_000
    print(f"Benchmark: converting '{test_input[:16]}...' ({number:,} iterations)\n")
    results = []
    for label, func in [("Lookup table", bin_to_hex_lookup),
                         ("Built-in", bin_to_hex_builtin),
                         ("Format string", bin_to_hex_format)]:
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
