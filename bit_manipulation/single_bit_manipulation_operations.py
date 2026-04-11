"""
Single bit manipulation operations: get, set, clear, flip a specific bit.

These four operations are the building blocks of nearly every bit manipulation
problem.  Each works on a 0-indexed bit position (bit 0 = LSB).

get_bit  -- extract the value (0 or 1) of a specific bit
set_bit  -- force a specific bit to 1
clear_bit -- force a specific bit to 0
flip_bit  -- toggle a specific bit (0->1, 1->0)

>>> get_bit(0b1010, 0)
0
>>> get_bit(0b1010, 1)
1
>>> get_bit(0b1010, 3)
1
>>> set_bit(0b1010, 0)
11
>>> set_bit(0b1010, 1)
10
>>> clear_bit(0b1010, 1)
8
>>> clear_bit(0b1010, 0)
10
>>> flip_bit(0b1010, 0)
11
>>> flip_bit(0b1010, 1)
8
"""


def get_bit(number: int, position: int) -> int:
    """
    Get the bit value at `position` (0-indexed from LSB).

    Shift right by `position` places, then AND with 1 to isolate the bit.

    >>> get_bit(0b1010, 0)
    0
    >>> get_bit(0b1010, 1)
    1
    >>> get_bit(0b1010, 2)
    0
    >>> get_bit(0b1010, 3)
    1
    >>> get_bit(0, 5)
    0
    >>> get_bit(0b11111, 4)
    1
    """
    return (number >> position) & 1


def set_bit(number: int, position: int) -> int:
    """
    Set the bit at `position` to 1.

    OR with a mask that has only the target bit set.

    >>> set_bit(0b1010, 0)
    11
    >>> set_bit(0b1010, 1)
    10
    >>> set_bit(0, 3)
    8
    >>> set_bit(0b1111, 2)
    15
    """
    return number | (1 << position)


def clear_bit(number: int, position: int) -> int:
    """
    Clear the bit at `position` (set it to 0).

    AND with the complement of a mask that has only the target bit set.

    >>> clear_bit(0b1010, 1)
    8
    >>> clear_bit(0b1010, 0)
    10
    >>> clear_bit(0b1010, 3)
    2
    >>> clear_bit(0, 5)
    0
    >>> clear_bit(0b1111, 2)
    11
    """
    return number & ~(1 << position)


def flip_bit(number: int, position: int) -> int:
    """
    Flip (toggle) the bit at `position`.

    XOR with a mask that has only the target bit set.

    >>> flip_bit(0b1010, 0)
    11
    >>> flip_bit(0b1010, 1)
    8
    >>> flip_bit(0b1010, 3)
    2
    >>> flip_bit(0, 0)
    1
    >>> flip_bit(0b1111, 2)
    11
    """
    return number ^ (1 << position)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
