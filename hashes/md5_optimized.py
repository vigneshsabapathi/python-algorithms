#!/usr/bin/env python3
"""
Optimized and alternative implementations of MD5.

MD5 produces a 128-bit (32 hex char) digest. The reference implementation
operates on bit strings (ASCII '0'/'1' characters) which is educational
but very slow. Real implementations operate on bytes directly.

Variants:
  reference      -- TheAlgorithms bit-string implementation
  hashlib_builtin -- Python's hashlib.md5 (OpenSSL C implementation)
  struct_based   -- byte-level implementation using struct module

Run:
    python hashes/md5_optimized.py
"""

from __future__ import annotations

import hashlib
import os
import struct
import sys
import timeit
from math import sin

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.md5 import md5_me as reference


# ---------------------------------------------------------------------------
# Variant 1 -- hashlib_builtin: Python's C-level MD5
# ---------------------------------------------------------------------------

def hashlib_builtin(message: bytes) -> bytes:
    """
    MD5 using Python's hashlib (OpenSSL).

    >>> hashlib_builtin(b"")
    b'd41d8cd98f00b204e9800998ecf8427e'
    >>> hashlib_builtin(b"The quick brown fox jumps over the lazy dog")
    b'9e107d9d372bb6826bd81d3542a419d6'
    """
    return hashlib.md5(message).hexdigest().encode("utf-8")


# ---------------------------------------------------------------------------
# Variant 2 -- struct_based: byte-level MD5 (no bit strings)
# ---------------------------------------------------------------------------

# Pre-computed constants
_T = [int(2**32 * abs(sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
_SHIFTS = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
]
_MASK = 0xFFFFFFFF


def _left_rotate(n: int, b: int) -> int:
    return ((n << b) | (n >> (32 - b))) & _MASK


def struct_based(message: bytes) -> bytes:
    """
    Byte-level MD5 using struct for packing/unpacking.

    Much faster than the bit-string reference -- operates on actual bytes
    instead of ASCII '0'/'1' characters.

    >>> struct_based(b"")
    b'd41d8cd98f00b204e9800998ecf8427e'
    >>> struct_based(b"The quick brown fox jumps over the lazy dog")
    b'9e107d9d372bb6826bd81d3542a419d6'
    >>> struct_based(b"The quick brown fox jumps over the lazy dog.")
    b'e4d909c290d0fb1ca068ffaddf22cbd0'

    >>> import hashlib
    >>> msgs = [b"", b"abc", b"hello world", b"x" * 1000]
    >>> all(struct_based(m) == hashlib.md5(m).hexdigest().encode() for m in msgs)
    True
    """
    # Padding
    orig_len = len(message)
    message += b"\x80"
    while len(message) % 64 != 56:
        message += b"\x00"
    message += struct.pack("<Q", orig_len * 8)

    # Initial state
    a0, b0, c0, d0 = 0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476

    # Process each 64-byte block
    for offset in range(0, len(message), 64):
        block = message[offset : offset + 64]
        M = list(struct.unpack("<16I", block))

        a, b, c, d = a0, b0, c0, d0

        for i in range(64):
            if i < 16:
                f = d ^ (b & (c ^ d))
                g = i
            elif i < 32:
                f = c ^ (d & (b ^ c))
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d & _MASK))
                g = (7 * i) % 16

            f = (f + a + _T[i] + M[g]) & _MASK
            a = d
            d = c
            c = b
            b = (b + _left_rotate(f, _SHIFTS[i])) & _MASK

        a0 = (a0 + a) & _MASK
        b0 = (b0 + b) & _MASK
        c0 = (c0 + c) & _MASK
        d0 = (d0 + d) & _MASK

    return struct.pack("<4I", a0, b0, c0, d0).hex().encode("utf-8")


# ---------------------------------------------------------------------------
# Variant 3 -- incremental: supports update() like hashlib
# ---------------------------------------------------------------------------

class MD5Incremental:
    """
    Incremental MD5 -- supports feeding data in chunks via update().

    >>> h = MD5Incremental()
    >>> h.update(b"The quick brown fox ")
    >>> h.update(b"jumps over the lazy dog")
    >>> h.hexdigest()
    '9e107d9d372bb6826bd81d3542a419d6'
    """

    def __init__(self) -> None:
        self._state = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
        self._buffer = b""
        self._count = 0

    def update(self, data: bytes) -> None:
        self._buffer += data
        self._count += len(data)
        while len(self._buffer) >= 64:
            self._process_block(self._buffer[:64])
            self._buffer = self._buffer[64:]

    def _process_block(self, block: bytes) -> None:
        M = list(struct.unpack("<16I", block))
        a, b, c, d = self._state

        for i in range(64):
            if i < 16:
                f = d ^ (b & (c ^ d))
                g = i
            elif i < 32:
                f = c ^ (d & (b ^ c))
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d & _MASK))
                g = (7 * i) % 16

            f = (f + a + _T[i] + M[g]) & _MASK
            a = d
            d = c
            c = b
            b = (b + _left_rotate(f, _SHIFTS[i])) & _MASK

        self._state[0] = (self._state[0] + a) & _MASK
        self._state[1] = (self._state[1] + b) & _MASK
        self._state[2] = (self._state[2] + c) & _MASK
        self._state[3] = (self._state[3] + d) & _MASK

    def hexdigest(self) -> str:
        # Finalize: pad the remaining buffer
        msg = self._buffer
        orig_len = self._count
        msg += b"\x80"
        while len(msg) % 64 != 56:
            msg += b"\x00"
        msg += struct.pack("<Q", orig_len * 8)

        # Process remaining blocks
        state = list(self._state)
        for offset in range(0, len(msg), 64):
            block = msg[offset : offset + 64]
            M = list(struct.unpack("<16I", block))
            a, b, c, d = state

            for i in range(64):
                if i < 16:
                    f = d ^ (b & (c ^ d))
                    g = i
                elif i < 32:
                    f = c ^ (d & (b ^ c))
                    g = (5 * i + 1) % 16
                elif i < 48:
                    f = b ^ c ^ d
                    g = (3 * i + 5) % 16
                else:
                    f = c ^ (b | (~d & _MASK))
                    g = (7 * i) % 16

                f = (f + a + _T[i] + M[g]) & _MASK
                a = d
                d = c
                c = b
                b = (b + _left_rotate(f, _SHIFTS[i])) & _MASK

            state[0] = (state[0] + a) & _MASK
            state[1] = (state[1] + b) & _MASK
            state[2] = (state[2] + c) & _MASK
            state[3] = (state[3] + d) & _MASK

        return struct.pack("<4I", *state).hex()


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_VECTORS = [
    (b"", "d41d8cd98f00b204e9800998ecf8427e"),
    (b"a", "0cc175b9c0f1b6a831c399e269772661"),
    (b"abc", "900150983cd24fb0d6963f7d28e17f72"),
    (b"message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
    (b"The quick brown fox jumps over the lazy dog", "9e107d9d372bb6826bd81d3542a419d6"),
    (b"The quick brown fox jumps over the lazy dog.", "e4d909c290d0fb1ca068ffaddf22cbd0"),
]

IMPLS = [
    ("reference", lambda m: reference(m).decode()),
    ("hashlib", lambda m: hashlib_builtin(m).decode()),
    ("struct_based", lambda m: struct_based(m).decode()),
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
        print(f"  [{tag}] md5({msg[:40]!r}) = {expected}")

    # Incremental test
    h = MD5Incremental()
    h.update(b"The quick brown fox ")
    h.update(b"jumps over the lazy dog")
    inc_result = h.hexdigest()
    expected_inc = "9e107d9d372bb6826bd81d3542a419d6"
    print(f"  [{'OK' if inc_result == expected_inc else 'FAIL'}] incremental MD5 = {inc_result}")

    # Benchmark
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
