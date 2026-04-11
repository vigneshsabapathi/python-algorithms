"""
Reverse bits of a 32-bit unsigned integer.

Given a 32-bit unsigned integer, return the integer obtained by reversing
all 32 bits.  This is LeetCode 190.

The standard approach iterates through each of the 32 bits, extracting the
least-significant bit of the input and appending it to the result from the
left.

Example:
    Input:  43261596  (binary: 00000010100101000001111010011100)
    Output: 964176192 (binary: 00111001011110000010100101000000)

>>> reverse_bits(43261596)
964176192
"""


def reverse_bits(n: int) -> int:
    """
    Reverse all 32 bits of n.

    Iterate 32 times: extract LSB of n, shift result left, OR in the bit,
    then shift n right.

    Time:  O(1)  — always exactly 32 iterations
    Space: O(1)

    >>> reverse_bits(43261596)
    964176192
    >>> reverse_bits(0)
    0
    >>> reverse_bits(4294967295)
    4294967295
    >>> reverse_bits(1)
    2147483648
    >>> reverse_bits(2147483648)
    1
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
