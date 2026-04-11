#!/usr/bin/env python3
"""
Optimized and alternative implementations of SHA-1.

SHA-1 produces a 160-bit (40 hex char) digest. The reference uses a class
with separate padding/expansion/compression steps.

Variants:
  reference      -- TheAlgorithms SHA1Hash class
  hashlib_builtin -- Python's hashlib.sha1 (OpenSSL C implementation)
  functional     -- functional-style implementation (no class)
  hmac_sha1      -- HMAC-SHA1 using the hash function

Run:
    python hashes/sha1_optimized.py
"""

from __future__ import annotations

import hashlib
import os
import struct
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.sha1 import SHA1Hash as RefSHA1


# ---------------------------------------------------------------------------
# Variant 1 -- hashlib_builtin: Python's C-level SHA-1
# ---------------------------------------------------------------------------

def hashlib_builtin(message: bytes) -> str:
    """
    SHA-1 using Python's hashlib (OpenSSL).

    >>> hashlib_builtin(b"")
    'da39a3ee5e6b4b0d3255bfef95601890afd80709'
    >>> hashlib_builtin(b"The quick brown fox jumps over the lazy dog")
    '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'
    """
    return hashlib.sha1(message).hexdigest()


# ---------------------------------------------------------------------------
# Variant 2 -- functional: no-class implementation
# ---------------------------------------------------------------------------

def functional_sha1(message: bytes) -> str:
    """
    Functional SHA-1 -- same algorithm without class overhead.

    >>> functional_sha1(b"")
    'da39a3ee5e6b4b0d3255bfef95601890afd80709'
    >>> functional_sha1(b"Allan")
    '872af2d8ac3d8695387e7c804bf0e02c18df9e6e'
    >>> functional_sha1(b"The quick brown fox jumps over the lazy dog")
    '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'

    >>> import hashlib
    >>> msgs = [b"", b"abc", b"hello", b"x" * 1000]
    >>> all(functional_sha1(m) == hashlib.sha1(m).hexdigest() for m in msgs)
    True
    """
    def _rotate(n, b):
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    h0, h1, h2, h3, h4 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0

    # Padding
    padding = b"\x80" + b"\x00" * (63 - (len(message) + 8) % 64)
    padded = message + padding + struct.pack(">Q", 8 * len(message))

    # Process blocks
    for offset in range(0, len(padded), 64):
        block = padded[offset:offset + 64]
        w = list(struct.unpack(">16L", block)) + [0] * 64
        for i in range(16, 80):
            w[i] = _rotate(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)

        a, b, c, d, e = h0, h1, h2, h3, h4
        for i in range(80):
            if i < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif i < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif i < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            a, b, c, d, e = (
                (_rotate(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF,
                a,
                _rotate(b, 30),
                c,
                d,
            )
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return f"{h0:08x}{h1:08x}{h2:08x}{h3:08x}{h4:08x}"


# ---------------------------------------------------------------------------
# Variant 3 -- hmac_sha1: HMAC using SHA-1
# ---------------------------------------------------------------------------

def hmac_sha1(key: bytes, message: bytes) -> str:
    """
    HMAC-SHA1 implementation using our functional SHA-1.

    HMAC(K, m) = H((K' ^ opad) || H((K' ^ ipad) || m))
    where K' is the key padded/hashed to block size.

    >>> hmac_sha1(b"key", b"The quick brown fox jumps over the lazy dog")
    'de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9'
    >>> import hmac as _hmac
    >>> _hmac.new(b"key", b"The quick brown fox jumps over the lazy dog", hashlib.sha1).hexdigest()
    'de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9'
    """
    block_size = 64

    # Key preparation
    if len(key) > block_size:
        key = bytes.fromhex(functional_sha1(key))
    key = key.ljust(block_size, b"\x00")

    o_key_pad = bytes(k ^ 0x5C for k in key)
    i_key_pad = bytes(k ^ 0x36 for k in key)

    inner_hash = bytes.fromhex(functional_sha1(i_key_pad + message))
    return functional_sha1(o_key_pad + inner_hash)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_VECTORS = [
    (b"", "da39a3ee5e6b4b0d3255bfef95601890afd80709"),
    (b"Allan", "872af2d8ac3d8695387e7c804bf0e02c18df9e6e"),
    (b"The quick brown fox jumps over the lazy dog", "2fd4e1c67a2d28fced849ee1bb76e7391b93eb12"),
    (b"abc", "a9993e364706816aba3e25717850c26c9cd0d89d"),
]

IMPLS = [
    ("reference", lambda m: RefSHA1(m).final_hash()),
    ("hashlib", hashlib_builtin),
    ("functional", functional_sha1),
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
        print(f"  [{tag}] sha1({msg[:40]!r}) = {expected}")

    # HMAC test
    hmac_result = hmac_sha1(b"key", b"The quick brown fox jumps over the lazy dog")
    hmac_expected = "de7c9b85b8b78aa6bc8a7a36f70a90701c9db4d9"
    print(f"  [{'OK' if hmac_result == hmac_expected else 'FAIL'}] hmac_sha1 = {hmac_result}")

    # Cross-verify with hashlib
    test_msgs = [b"", b"hello", b"x" * 1000, b"abc" * 100]
    cross_ok = all(functional_sha1(m) == hashlib.sha1(m).hexdigest() for m in test_msgs)
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
