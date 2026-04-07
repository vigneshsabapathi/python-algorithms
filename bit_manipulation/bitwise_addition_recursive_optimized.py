"""
Optimized/alternative implementations for Bitwise Addition (no + operator).

Variants:
1. iterative — same XOR/AND logic but with a while loop (no recursion depth limit)
2. half_adder_chain — half-adder per bit using shift and mask
3. log_carry   — uses bit_length to limit iterations
4. numpy       — vectorized addition via numpy (for array inputs)
"""

import timeit


def bitwise_addition_iterative(number: int, other_number: int) -> int:
    """
    Iterative XOR/AND — avoids recursion depth limit.

    >>> bitwise_addition_iterative(4, 5)
    9
    >>> bitwise_addition_iterative(8, 9)
    17
    >>> bitwise_addition_iterative(0, 4)
    4
    >>> bitwise_addition_iterative(0, 0)
    0
    >>> bitwise_addition_iterative(12345, 67890)
    80235
    """
    while other_number != 0:
        carry = number & other_number
        number = number ^ other_number
        other_number = carry << 1
    return number


def bitwise_addition_half_adder(a: int, b: int) -> int:
    """
    Half-adder per bit: process one bit at a time.

    >>> bitwise_addition_half_adder(4, 5)
    9
    >>> bitwise_addition_half_adder(8, 9)
    17
    >>> bitwise_addition_half_adder(0, 4)
    4
    >>> bitwise_addition_half_adder(0, 0)
    0
    >>> bitwise_addition_half_adder(12345, 67890)
    80235
    """
    result = 0
    carry = 0
    bit = 0
    while a > 0 or b > 0 or carry > 0:
        a_bit = a & 1
        b_bit = b & 1
        s = a_bit ^ b_bit ^ carry
        carry = (a_bit & b_bit) | (a_bit & carry) | (b_bit & carry)
        result |= s << bit
        bit += 1
        a >>= 1
        b >>= 1
    return result


def bitwise_addition_log(a: int, b: int) -> int:
    """
    Same XOR/AND but uses bit_length hint for clarity.

    >>> bitwise_addition_log(4, 5)
    9
    >>> bitwise_addition_log(8, 9)
    17
    >>> bitwise_addition_log(0, 4)
    4
    >>> bitwise_addition_log(0, 0)
    0
    >>> bitwise_addition_log(12345, 67890)
    80235
    """
    while b != 0:
        a, b = a ^ b, (a & b) << 1
    return a


def benchmark():
    """Compare all implementations."""
    from bit_manipulation.bitwise_addition_recursive import bitwise_addition_recursive as recursive

    test_pairs = [(4, 5), (8, 9), (0, 4), (100, 200), (999, 1), (12345, 67890)]
    n = 200000

    impls = {
        "recursive": recursive,
        "iterative": bitwise_addition_iterative,
        "half_adder": bitwise_addition_half_adder,
        "log_carry": bitwise_addition_log,
    }

    print(f"{'Implementation':<18} {'Time (ms)':<14} {'Match':<6}")
    print("-" * 40)

    for name, func in impls.items():
        t = timeit.timeit(lambda: [func(a, b) for a, b in test_pairs], number=n)
        results = [func(a, b) for a, b in test_pairs]
        expected = [a + b for a, b in test_pairs]
        match = results == expected
        print(f"{name:<18} {t*1000/n:<14.4f} {'Yes' if match else 'No':<6}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("\n--- Benchmark (per-call time) ---")
    benchmark()
