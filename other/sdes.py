"""
Simplified DES (S-DES) — Educational symmetric-key block cipher.

S-DES is a simplified version of DES designed for teaching. It uses
an 8-bit plaintext block and a 10-bit key, performing two rounds of
Feistel operations.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/sdes.py
"""

from __future__ import annotations

# Permutation tables
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]

S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2],
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3],
]


def permute(data: list[int], table: list[int]) -> list[int]:
    """
    Apply a permutation table to data.

    >>> permute([1, 0, 1, 0, 0, 1, 1, 0, 0, 1], P10)
    [1, 0, 0, 1, 0, 1, 1, 0, 0, 1]
    """
    return [data[i - 1] for i in table]


def left_shift(bits: list[int], n: int) -> list[int]:
    """
    Circular left shift.

    >>> left_shift([1, 0, 1, 0, 0], 1)
    [0, 1, 0, 0, 1]
    """
    return bits[n:] + bits[:n]


def xor(a: list[int], b: list[int]) -> list[int]:
    """XOR two bit lists."""
    return [x ^ y for x, y in zip(a, b)]


def sbox_lookup(bits: list[int], sbox: list[list[int]]) -> list[int]:
    """Look up 4-bit input in S-box, return 2-bit output."""
    row = bits[0] * 2 + bits[3]
    col = bits[1] * 2 + bits[2]
    val = sbox[row][col]
    return [val >> 1, val & 1]


def generate_keys(key: list[int]) -> tuple[list[int], list[int]]:
    """
    Generate two 8-bit subkeys from a 10-bit key.

    >>> generate_keys([1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
    ([1, 0, 1, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0, 1, 1])
    """
    p10 = permute(key, P10)
    left, right = p10[:5], p10[5:]

    # LS-1
    left1, right1 = left_shift(left, 1), left_shift(right, 1)
    k1 = permute(left1 + right1, P8)

    # LS-2
    left2, right2 = left_shift(left1, 2), left_shift(right1, 2)
    k2 = permute(left2 + right2, P8)

    return k1, k2


def fk(data: list[int], key: list[int]) -> list[int]:
    """Apply the Feistel function fK."""
    left, right = data[:4], data[4:]
    ep = permute(right, EP)
    xored = xor(ep, key)

    s0_out = sbox_lookup(xored[:4], S0)
    s1_out = sbox_lookup(xored[4:], S1)

    p4 = permute(s0_out + s1_out, P4)
    return xor(left, p4) + right


def encrypt(plaintext: list[int], key: list[int]) -> list[int]:
    """
    Encrypt 8-bit plaintext with 10-bit key using S-DES.

    >>> encrypt([1, 0, 1, 0, 0, 1, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
    [1, 1, 0, 0, 1, 0, 1, 0]
    """
    k1, k2 = generate_keys(key)

    ip = permute(plaintext, IP)
    after_fk1 = fk(ip, k1)
    swapped = after_fk1[4:] + after_fk1[:4]  # SW
    after_fk2 = fk(swapped, k2)
    ciphertext = permute(after_fk2, IP_INV)

    return ciphertext


def decrypt(ciphertext: list[int], key: list[int]) -> list[int]:
    """
    Decrypt 8-bit ciphertext with 10-bit key using S-DES.

    >>> decrypt([1, 1, 0, 0, 1, 0, 1, 0], [1, 0, 1, 0, 0, 0, 0, 0, 1, 0])
    [1, 0, 1, 0, 0, 1, 0, 1]
    """
    k1, k2 = generate_keys(key)

    ip = permute(ciphertext, IP)
    after_fk2 = fk(ip, k2)
    swapped = after_fk2[4:] + after_fk2[:4]
    after_fk1 = fk(swapped, k1)
    plaintext = permute(after_fk1, IP_INV)

    return plaintext


if __name__ == "__main__":
    import doctest

    doctest.testmod()
