"""
Swap all odd and even bits of a number.

Given a number, swap its odd-position bits with even-position bits.
Even bits (0, 2, 4, ...) shift left by 1; odd bits (1, 3, 5, ...) shift right by 1.

Using masks:
  0xAAAAAAAA = 1010 1010 ... — selects even-position bits (0, 2, 4, ...)
  0x55555555 = 0101 0101 ... — selects odd-position bits (1, 3, 5, ...)

Example:
  23  = 0b00010111
        even bits (pos 0,2,4): 1_1_1 → shift left  → _1_1_1
        odd  bits (pos 1,3):   _0_1_ → shift right → 0_1___
        result: 0b00101011 = 43

>>> swap_all_odd_and_even_bits(23)
43
>>> swap_all_odd_and_even_bits(2)
1
>>> swap_all_odd_and_even_bits(0)
0
>>> swap_all_odd_and_even_bits(1)
2
>>> swap_all_odd_and_even_bits(3)
3
>>> swap_all_odd_and_even_bits(4)
8
>>> swap_all_odd_and_even_bits(5)
10
>>> swap_all_odd_and_even_bits(6)
9
>>> swap_all_odd_and_even_bits(0xFF)
255
"""


def swap_all_odd_and_even_bits(num: int) -> int:
    """
    Swap all odd-position bits with even-position bits.

    Uses 32-bit masks to separate even and odd bits, then shifts
    and recombines with OR.

    >>> swap_all_odd_and_even_bits(23)
    43
    >>> swap_all_odd_and_even_bits(2)
    1
    >>> swap_all_odd_and_even_bits(0)
    0
    >>> swap_all_odd_and_even_bits(1)
    2
    >>> swap_all_odd_and_even_bits(3)
    3
    >>> swap_all_odd_and_even_bits(4)
    8
    >>> swap_all_odd_and_even_bits(5)
    10
    >>> swap_all_odd_and_even_bits(6)
    9
    """
    # 0xAAAAAAAA selects bits at even positions (0, 2, 4, ...)
    even_bits = num & 0xAAAAAAAA
    # 0x55555555 selects bits at odd positions (1, 3, 5, ...)
    odd_bits = num & 0x55555555

    # Shift even bits right by 1 (move to odd positions)
    # Shift odd bits left by 1 (move to even positions)
    return (even_bits >> 1) | (odd_bits << 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
