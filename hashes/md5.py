"""
MD5 (Message-Digest Algorithm 5) -- a hash function producing a 128-bit
(16-byte) hash value, typically expressed as a 32-character hex string.

The algorithm processes a message in blocks of 512 bits, padding as needed.
It uses 4 auxiliary functions (F, G, H, I) and 64 rounds of mixing operations
on a 128-bit state (four 32-bit words: a, b, c, d).

Although MD5 was used as a cryptographic hash function in the past, it has
been broken and should NOT be used for security purposes.

For more info, see https://en.wikipedia.org/wiki/MD5
"""

from collections.abc import Generator
from math import sin


def to_little_endian(string_32: bytes) -> bytes:
    """
    Converts a 32-char byte string to little-endian in groups of 8 chars.

    >>> to_little_endian(b'1234567890abcdfghijklmnopqrstuvw')
    b'pqrstuvwhijklmno90abcdfg12345678'
    >>> to_little_endian(b'1234567890')
    Traceback (most recent call last):
    ...
    ValueError: Input must be of length 32
    """
    if len(string_32) != 32:
        raise ValueError("Input must be of length 32")
    little_endian = b""
    for i in [3, 2, 1, 0]:
        little_endian += string_32[8 * i : 8 * i + 8]
    return little_endian


def reformat_hex(i: int) -> bytes:
    """
    Converts a non-negative integer to 8-char little-endian hex string.

    >>> reformat_hex(1234)
    b'd2040000'
    >>> reformat_hex(0)
    b'00000000'
    >>> reformat_hex(-1)
    Traceback (most recent call last):
    ...
    ValueError: Input must be non-negative
    """
    if i < 0:
        raise ValueError("Input must be non-negative")
    hex_rep = format(i, "08x")[-8:]
    little_endian_hex = b""
    for j in [3, 2, 1, 0]:
        little_endian_hex += hex_rep[2 * j : 2 * j + 2].encode("utf-8")
    return little_endian_hex


def preprocess(message: bytes) -> bytes:
    """
    Preprocess message: convert to bits, pad to multiple of 512.

    >>> preprocess(b"a") == (b"01100001" + b"1" +
    ...                     (b"0" * 439) + b"00001000" + (b"0" * 56))
    True
    >>> preprocess(b"") == b"1" + (b"0" * 447) + (b"0" * 64)
    True
    """
    bit_string = b""
    for char in message:
        bit_string += format(char, "08b").encode("utf-8")
    start_len = format(len(bit_string), "064b").encode("utf-8")
    bit_string += b"1"
    while len(bit_string) % 512 != 448:
        bit_string += b"0"
    bit_string += to_little_endian(start_len[32:]) + to_little_endian(start_len[:32])
    return bit_string


def get_block_words(bit_string: bytes) -> Generator[list[int]]:
    """
    Split bit string into 512-bit blocks and yield each as 16 32-bit words.

    >>> test_string = ("".join(format(n << 24, "032b") for n in range(16))
    ...                  .encode("utf-8"))
    >>> list(get_block_words(test_string))
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]]
    >>> list(get_block_words(b""))
    []
    >>> list(get_block_words(b"1111"))
    Traceback (most recent call last):
    ...
    ValueError: Input must have length that's a multiple of 512
    """
    if len(bit_string) % 512 != 0:
        raise ValueError("Input must have length that's a multiple of 512")
    for pos in range(0, len(bit_string), 512):
        block = bit_string[pos : pos + 512]
        block_words = []
        for i in range(0, 512, 32):
            block_words.append(int(to_little_endian(block[i : i + 32]), 2))
        yield block_words


def not_32(i: int) -> int:
    """
    Bitwise NOT on a 32-bit unsigned integer.

    >>> not_32(34)
    4294967261
    >>> not_32(0)
    4294967295
    >>> not_32(-1)
    Traceback (most recent call last):
    ...
    ValueError: Input must be non-negative
    """
    if i < 0:
        raise ValueError("Input must be non-negative")
    i_str = format(i, "032b")
    new_str = ""
    for c in i_str:
        new_str += "1" if c == "0" else "0"
    return int(new_str, 2)


def sum_32(a: int, b: int) -> int:
    """
    Add two numbers as unsigned 32-bit integers.

    >>> sum_32(1, 1)
    2
    >>> sum_32(4294967295, 1)
    0
    """
    return (a + b) % 2**32


def left_rotate_32(i: int, shift: int) -> int:
    """
    Left-rotate a 32-bit unsigned integer by shift bits.

    >>> left_rotate_32(1234, 1)
    2468
    >>> left_rotate_32(2147483648, 1)
    1
    >>> left_rotate_32(-1, 0)
    Traceback (most recent call last):
    ...
    ValueError: Input must be non-negative
    >>> left_rotate_32(0, -1)
    Traceback (most recent call last):
    ...
    ValueError: Shift must be non-negative
    """
    if i < 0:
        raise ValueError("Input must be non-negative")
    if shift < 0:
        raise ValueError("Shift must be non-negative")
    return ((i << shift) ^ (i >> (32 - shift))) % 2**32


def md5_me(message: bytes) -> bytes:
    """
    Returns the 32-char MD5 hash of a given message.

    >>> md5_me(b"")
    b'd41d8cd98f00b204e9800998ecf8427e'
    >>> md5_me(b"The quick brown fox jumps over the lazy dog")
    b'9e107d9d372bb6826bd81d3542a419d6'
    >>> md5_me(b"The quick brown fox jumps over the lazy dog.")
    b'e4d909c290d0fb1ca068ffaddf22cbd0'

    >>> import hashlib
    >>> from string import ascii_letters
    >>> msgs = [b"", ascii_letters.encode("utf-8"), b"The quick brown fox jumps over the lazy dog."]
    >>> all(md5_me(msg) == hashlib.md5(msg).hexdigest().encode("utf-8") for msg in msgs)
    True
    """
    bit_string = preprocess(message)
    added_consts = [int(2**32 * abs(sin(i + 1))) for i in range(64)]

    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476

    shift_amounts = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
    ]

    for block_words in get_block_words(bit_string):
        a, b, c, d = a0, b0, c0, d0
        for i in range(64):
            if i <= 15:
                f = d ^ (b & (c ^ d))
                g = i
            elif i <= 31:
                f = c ^ (d & (b ^ c))
                g = (5 * i + 1) % 16
            elif i <= 47:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | not_32(d))
                g = (7 * i) % 16
            f = (f + a + added_consts[i] + block_words[g]) % 2**32
            a = d
            d = c
            c = b
            b = sum_32(b, left_rotate_32(f, shift_amounts[i]))
        a0 = sum_32(a0, a)
        b0 = sum_32(b0, b)
        c0 = sum_32(c0, c)
        d0 = sum_32(d0, d)

    return reformat_hex(a0) + reformat_hex(b0) + reformat_hex(c0) + reformat_hex(d0)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
