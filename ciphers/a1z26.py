"""
A1Z26 Cipher — Letter-Number cipher where A=1, B=2, ..., Z=26.

Each character maps to its 1-based position in the alphabet.

References:
    https://www.dcode.fr/letter-number-cipher
    http://bestcodes.weebly.com/a1z26.html
"""

from __future__ import annotations


def encode(plain: str) -> list[int]:
    """
    Encode a lowercase string to a list of 1-based alphabet positions.

    >>> encode("myname")
    [13, 25, 14, 1, 13, 5]
    >>> encode("abc")
    [1, 2, 3]
    >>> encode("z")
    [26]
    """
    return [ord(elem) - 96 for elem in plain]


def decode(encoded: list[int]) -> str:
    """
    Decode a list of 1-based alphabet positions back to a lowercase string.

    >>> decode([13, 25, 14, 1, 13, 5])
    'myname'
    >>> decode([1, 2, 3])
    'abc'
    >>> decode([26])
    'z'
    """
    return "".join(chr(elem + 96) for elem in encoded)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
