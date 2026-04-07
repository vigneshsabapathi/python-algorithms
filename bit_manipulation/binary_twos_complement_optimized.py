"""
Optimized/alternative implementations for Two's Complement.

Variants:
1. bit_length — uses Python's bit_length() for minimal-width representation
2. bitwise_not_mask — (~n + 1) masked to appropriate width
3. ctypes_uint32 — fixed 32-bit two's complement via ctypes
4. bit_flip_add1 — manual: flip all bits then add 1 (classic textbook)
"""

import ctypes
import timeit


def twos_complement_bit_length(number: int) -> str:
    """
    Use bit_length() for minimal-width two's complement.

    >>> twos_complement_bit_length(0)
    '0b0'
    >>> twos_complement_bit_length(-1)
    '0b11'
    >>> twos_complement_bit_length(-5)
    '0b1011'
    >>> twos_complement_bit_length(-17)
    '0b101111'
    >>> twos_complement_bit_length(-207)
    '0b100110001'
    >>> twos_complement_bit_length(1)
    Traceback (most recent call last):
        ...
    ValueError: input must be a negative integer
    """
    if number > 0:
        raise ValueError("input must be a negative integer")
    if number == 0:
        return "0b0"
    bits = number.bit_length()
    return bin(number & ((1 << bits) - 1) | (1 << bits))


def twos_complement_bitwise_not_mask(number: int) -> str:
    """
    Classic: (~abs_val + 1) masked to bit_length width.

    >>> twos_complement_bitwise_not_mask(0)
    '0b0'
    >>> twos_complement_bitwise_not_mask(-1)
    '0b11'
    >>> twos_complement_bitwise_not_mask(-5)
    '0b1011'
    >>> twos_complement_bitwise_not_mask(-17)
    '0b101111'
    >>> twos_complement_bitwise_not_mask(-207)
    '0b100110001'
    >>> twos_complement_bitwise_not_mask(1)
    Traceback (most recent call last):
        ...
    ValueError: input must be a negative integer
    """
    if number > 0:
        raise ValueError("input must be a negative integer")
    if number == 0:
        return "0b0"
    abs_val = abs(number)
    bits = abs_val.bit_length()
    mask = (1 << bits) - 1
    result = (~abs_val + 1) & mask | (1 << bits)
    return bin(result)


def twos_complement_ctypes32(number: int) -> str:
    """
    Fixed 32-bit two's complement using ctypes (matches CPU representation).

    >>> twos_complement_ctypes32(0)
    '0b0'
    >>> twos_complement_ctypes32(-1)
    '0b11111111111111111111111111111111'
    >>> twos_complement_ctypes32(-5)
    '0b11111111111111111111111111111011'
    >>> twos_complement_ctypes32(1)
    Traceback (most recent call last):
        ...
    ValueError: input must be a negative integer
    """
    if number > 0:
        raise ValueError("input must be a negative integer")
    if number == 0:
        return "0b0"
    return bin(ctypes.c_uint32(number).value)


def twos_complement_bit_flip_add1(number: int) -> str:
    """
    Manual textbook method: flip all bits of abs value, add 1.

    >>> twos_complement_bit_flip_add1(0)
    '0b0'
    >>> twos_complement_bit_flip_add1(-1)
    '0b11'
    >>> twos_complement_bit_flip_add1(-5)
    '0b1011'
    >>> twos_complement_bit_flip_add1(-17)
    '0b101111'
    >>> twos_complement_bit_flip_add1(-207)
    '0b100110001'
    >>> twos_complement_bit_flip_add1(1)
    Traceback (most recent call last):
        ...
    ValueError: input must be a negative integer
    """
    if number > 0:
        raise ValueError("input must be a negative integer")
    if number == 0:
        return "0b0"
    abs_val = abs(number)
    bits = abs_val.bit_length()
    flipped = ((1 << bits) - 1) ^ abs_val  # XOR to flip bits
    result = flipped + 1
    return bin(result | (1 << bits))


def benchmark():
    """Compare all implementations."""
    from bit_manipulation.binary_twos_complement import twos_complement as original

    test_vals = [-1, -5, -17, -207, -1024, -65535]
    n = 100000

    impls = {
        "original": original,
        "bit_length": twos_complement_bit_length,
        "bitwise_not_mask": twos_complement_bitwise_not_mask,
        "bit_flip_add1": twos_complement_bit_flip_add1,
    }

    print(f"{'Implementation':<22} {'Time (ms)':<12} {'Match':<6}")
    print("-" * 42)

    for name, func in impls.items():
        t = timeit.timeit(lambda: [func(v) for v in test_vals], number=n)
        results = [func(v) for v in test_vals]
        expected = [original(v) for v in test_vals]
        match = results == expected
        print(f"{name:<22} {t*1000/n:<12.4f} {'Yes' if match else 'No':<6}")

    # ctypes is fixed 32-bit, so compare separately
    t = timeit.timeit(
        lambda: [twos_complement_ctypes32(v) for v in test_vals], number=n
    )
    print(f"{'ctypes_uint32':<22} {t*1000/n:<12.4f} {'N/A (32-bit)':<6}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("\n--- Benchmark (per-call time) ---")
    benchmark()
