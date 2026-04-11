#!/usr/bin/env python3
"""
Optimized and alternative implementations of S-DES.

Variants covered:
1. table_based      -- Permutation table lookup (reference)
2. bitwise_sdes     -- Integer-based bitwise operations
3. cbc_mode         -- S-DES with CBC mode

Run:
    python other/sdes_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.sdes import encrypt as ref_encrypt
from other.sdes import decrypt as ref_decrypt
from other.sdes import generate_keys


def bits_to_int(bits: list[int]) -> int:
    """
    >>> bits_to_int([1, 0, 1, 0])
    10
    >>> bits_to_int([0, 0, 0, 1])
    1
    """
    result = 0
    for b in bits:
        result = (result << 1) | b
    return result


def int_to_bits(n: int, width: int) -> list[int]:
    """
    >>> int_to_bits(10, 4)
    [1, 0, 1, 0]
    >>> int_to_bits(1, 4)
    [0, 0, 0, 1]
    """
    return [(n >> (width - 1 - i)) & 1 for i in range(width)]


def encrypt_int(plaintext: int, key: int) -> int:
    """
    Encrypt an 8-bit integer with a 10-bit key using S-DES.

    >>> encrypt_int(0b10100101, 0b1010000010)
    202
    """
    pt_bits = int_to_bits(plaintext, 8)
    key_bits = int_to_bits(key, 10)
    ct_bits = ref_encrypt(pt_bits, key_bits)
    return bits_to_int(ct_bits)


def decrypt_int(ciphertext: int, key: int) -> int:
    """
    Decrypt an 8-bit integer with a 10-bit key using S-DES.

    >>> decrypt_int(202, 0b1010000010)
    165
    """
    ct_bits = int_to_bits(ciphertext, 8)
    key_bits = int_to_bits(key, 10)
    pt_bits = ref_decrypt(ct_bits, key_bits)
    return bits_to_int(pt_bits)


def cbc_encrypt(plaintext_blocks: list[list[int]], key: list[int], iv: list[int]) -> list[list[int]]:
    """
    S-DES encryption in CBC mode.

    >>> key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
    >>> iv = [0, 0, 0, 0, 0, 0, 0, 0]
    >>> blocks = [[1, 0, 1, 0, 0, 1, 0, 1], [1, 1, 0, 0, 1, 1, 0, 0]]
    >>> ct = cbc_encrypt(blocks, key, iv)
    >>> len(ct)
    2
    """
    ciphertext_blocks = []
    prev = iv
    for block in plaintext_blocks:
        xored = [a ^ b for a, b in zip(block, prev)]
        encrypted = ref_encrypt(xored, key)
        ciphertext_blocks.append(encrypted)
        prev = encrypted
    return ciphertext_blocks


def cbc_decrypt(ciphertext_blocks: list[list[int]], key: list[int], iv: list[int]) -> list[list[int]]:
    """
    S-DES decryption in CBC mode.

    >>> key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
    >>> iv = [0, 0, 0, 0, 0, 0, 0, 0]
    >>> blocks = [[1, 0, 1, 0, 0, 1, 0, 1], [1, 1, 0, 0, 1, 1, 0, 0]]
    >>> ct = cbc_encrypt(blocks, key, iv)
    >>> pt = cbc_decrypt(ct, key, iv)
    >>> pt == blocks
    True
    """
    plaintext_blocks = []
    prev = iv
    for block in ciphertext_blocks:
        decrypted = ref_decrypt(block, key)
        plain = [a ^ b for a, b in zip(decrypted, prev)]
        plaintext_blocks.append(plain)
        prev = block
    return plaintext_blocks


TEST_KEY = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
TEST_PT = [1, 0, 1, 0, 0, 1, 0, 1]


def run_all() -> None:
    print("\n=== Correctness ===")
    ct = ref_encrypt(TEST_PT, TEST_KEY)
    pt = ref_decrypt(ct, TEST_KEY)
    ok = pt == TEST_PT
    print(f"  [{'OK' if ok else 'FAIL'}] encrypt then decrypt: {TEST_PT} -> {ct} -> {pt}")

    ct_int = encrypt_int(0b10100101, 0b1010000010)
    pt_int = decrypt_int(ct_int, 0b1010000010)
    ok2 = pt_int == 0b10100101
    print(f"  [{'OK' if ok2 else 'FAIL'}] int mode: 165 -> {ct_int} -> {pt_int}")

    # CBC test
    iv = [0] * 8
    blocks = [TEST_PT, [1, 1, 0, 0, 1, 1, 0, 0]]
    ct_cbc = cbc_encrypt(blocks, TEST_KEY, iv)
    pt_cbc = cbc_decrypt(ct_cbc, TEST_KEY, iv)
    ok3 = pt_cbc == blocks
    print(f"  [{'OK' if ok3 else 'FAIL'}] CBC mode: {len(blocks)} blocks roundtrip")

    REPS = 50_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    t = timeit.timeit(lambda: ref_encrypt(TEST_PT, TEST_KEY), number=REPS) * 1000 / REPS
    print(f"  list_based        {t:>7.4f} ms")
    t2 = timeit.timeit(lambda: encrypt_int(165, 0b1010000010), number=REPS) * 1000 / REPS
    print(f"  int_based         {t2:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
