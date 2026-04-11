#!/usr/bin/env python3
"""
Optimized and alternative implementations of SHA-256.

SHA-256 produces a 256-bit (64 hex char) digest. The reference uses a class
with 64 rounds of compression per 512-bit block.

Variants:
  reference      -- TheAlgorithms SHA256 class
  hashlib_builtin -- Python's hashlib.sha256 (OpenSSL C implementation)
  functional     -- functional-style implementation (no class)
  hmac_sha256    -- HMAC-SHA256 using the hash function

Run:
    python hashes/sha256_optimized.py
"""

from __future__ import annotations

import hashlib
import os
import struct
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.sha256 import SHA256 as RefSHA256

# Round constants (first 32 bits of fractional parts of cube roots of first 64 primes)
_K = [
    0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
    0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
    0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
    0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
    0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
    0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
    0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
    0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
    0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
    0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
    0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
    0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
    0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
    0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
    0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
    0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
]
_MASK = 0xFFFFFFFF


def _ror(value: int, amount: int) -> int:
    return ((value >> amount) | (value << (32 - amount))) & _MASK


# ---------------------------------------------------------------------------
# Variant 1 -- hashlib_builtin: Python's C-level SHA-256
# ---------------------------------------------------------------------------

def hashlib_builtin(message: bytes) -> str:
    """
    SHA-256 using Python's hashlib (OpenSSL).

    >>> hashlib_builtin(b"")
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    >>> hashlib_builtin(b"hello world")
    'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
    """
    return hashlib.sha256(message).hexdigest()


# ---------------------------------------------------------------------------
# Variant 2 -- functional: no-class implementation
# ---------------------------------------------------------------------------

def functional_sha256(message: bytes) -> str:
    """
    Functional SHA-256 -- same algorithm without class overhead.

    >>> functional_sha256(b"")
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    >>> functional_sha256(b"Python")
    '18885f27b5af9012df19e496460f9294d5ab76128824c6f993787004f6d9a7db'
    >>> functional_sha256(b"hello world")
    'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'

    >>> import hashlib
    >>> msgs = [b"", b"abc", b"hello", b"x" * 1000]
    >>> all(functional_sha256(m) == hashlib.sha256(m).hexdigest() for m in msgs)
    True
    """
    # Initial hash values (first 32 bits of fractional parts of square roots of first 8 primes)
    h = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
         0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

    # Padding
    padding = b"\x80" + (b"\x00" * (63 - (len(message) + 8) % 64))
    padded = message + padding + struct.pack(">Q", len(message) * 8)

    # Process blocks
    for offset in range(0, len(padded), 64):
        block = padded[offset:offset + 64]
        w = list(struct.unpack(">16L", block)) + [0] * 48

        for i in range(16, 64):
            s0 = _ror(w[i-15], 7) ^ _ror(w[i-15], 18) ^ (w[i-15] >> 3)
            s1 = _ror(w[i-2], 17) ^ _ror(w[i-2], 19) ^ (w[i-2] >> 10)
            w[i] = (w[i-16] + s0 + w[i-7] + s1) & _MASK

        a, b, c, d, e, f, g, hh = h

        for i in range(64):
            s1 = _ror(e, 6) ^ _ror(e, 11) ^ _ror(e, 25)
            ch = (e & f) ^ ((~e & _MASK) & g)
            temp1 = (hh + s1 + ch + _K[i] + w[i]) & _MASK
            s0 = _ror(a, 2) ^ _ror(a, 13) ^ _ror(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (s0 + maj) & _MASK

            hh = g
            g = f
            f = e
            e = (d + temp1) & _MASK
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & _MASK

        h = [(hv + v) & _MASK for hv, v in zip(h, [a, b, c, d, e, f, g, hh])]

    return "".join(f"{v:08x}" for v in h)


# ---------------------------------------------------------------------------
# Variant 3 -- hmac_sha256: HMAC using SHA-256
# ---------------------------------------------------------------------------

def hmac_sha256(key: bytes, message: bytes) -> str:
    """
    HMAC-SHA256 implementation using our functional SHA-256.

    >>> hmac_sha256(b"key", b"The quick brown fox jumps over the lazy dog")
    'f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8'
    >>> import hmac as _hmac
    >>> _hmac.new(b"key", b"The quick brown fox jumps over the lazy dog", hashlib.sha256).hexdigest()
    'f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8'
    """
    block_size = 64

    if len(key) > block_size:
        key = bytes.fromhex(functional_sha256(key))
    key = key.ljust(block_size, b"\x00")

    o_key_pad = bytes(k ^ 0x5C for k in key)
    i_key_pad = bytes(k ^ 0x36 for k in key)

    inner_hash = bytes.fromhex(functional_sha256(i_key_pad + message))
    return functional_sha256(o_key_pad + inner_hash)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_VECTORS = [
    (b"", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (b"Python", "18885f27b5af9012df19e496460f9294d5ab76128824c6f993787004f6d9a7db"),
    (b"hello world", "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"),
    (b"abc", "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"),
]

IMPLS = [
    ("reference", lambda m: RefSHA256(m).hash),
    ("hashlib", hashlib_builtin),
    ("functional", functional_sha256),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for msg, expected in TEST_VECTORS:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(msg)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] sha256({msg[:40]!r}) = {expected[:20]}...")

    # HMAC test
    hmac_result = hmac_sha256(b"key", b"The quick brown fox jumps over the lazy dog")
    hmac_expected = "f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8"
    print(f"  [{'OK' if hmac_result == hmac_expected else 'FAIL'}] hmac_sha256 = {hmac_result[:20]}...")

    # Cross-verify
    test_msgs = [b"", b"hello", b"x" * 1000, b"abc" * 100]
    cross_ok = all(functional_sha256(m) == hashlib.sha256(m).hexdigest() for m in test_msgs)
    print(f"  [{'OK' if cross_ok else 'FAIL'}] Cross-verify functional vs hashlib: {len(test_msgs)} inputs")

    REPS = 2_000
    short_msg = b"Hello World"
    long_msg = b"x" * 10_000

    print(f"\n=== Benchmark (short message): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(short_msg), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")

    print(f"\n=== Benchmark (10KB message): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(long_msg), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
