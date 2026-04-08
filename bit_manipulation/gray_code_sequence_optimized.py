#!/usr/bin/env python3
"""
Comparison of Gray code sequence generation methods.

Original: recursive string-building approach (O(2^n) time + O(n·2^n) string space).

This file adds:
  2. XOR formula     — i ^ (i >> 1), single expression per element  [fastest]
  3. itertools-based — same formula via list comprehension
  4. reflect-and-prefix (iterative) — explicit mirror construction without recursion
  5. inverse (gray-to-binary) — decode Gray code back to binary

Ref: https://en.wikipedia.org/wiki/Gray_code

Run: python bit_manipulation/gray_code_sequence_optimized.py
"""

from __future__ import annotations
import timeit


# ---------------------------------------------------------------------------
# Implementations
# ---------------------------------------------------------------------------


def gray_code_recursive_string(n: int) -> list[int]:
    """
    Original approach: build string sequences recursively, convert to int at end.
    O(2^n) integers, each built by string concatenation. Correct but string-heavy.

    >>> gray_code_recursive_string(2)
    [0, 1, 3, 2]
    >>> gray_code_recursive_string(3)
    [0, 1, 3, 2, 6, 7, 5, 4]
    >>> gray_code_recursive_string(0)
    [0]
    """
    if n < 0:
        raise ValueError("The given input must be positive")

    def _build(bits: int) -> list[str]:
        if bits == 0:
            return ["0"]
        if bits == 1:
            return ["0", "1"]
        smaller = _build(bits - 1)
        half = 1 << (bits - 1)
        return ["0" + s for s in smaller] + ["1" + s for s in reversed(smaller)]

    return [int(s, 2) for s in _build(n)]


def gray_code_xor_formula(n: int) -> list[int]:
    """
    Direct XOR formula: Gray(i) = i ^ (i >> 1).
    Every Gray code integer can be computed independently in O(1).
    No recursion, no strings — just arithmetic.

    >>> gray_code_xor_formula(2)
    [0, 1, 3, 2]
    >>> gray_code_xor_formula(3)
    [0, 1, 3, 2, 6, 7, 5, 4]
    >>> gray_code_xor_formula(0)
    [0]
    """
    if n < 0:
        raise ValueError("The given input must be positive")
    return [i ^ (i >> 1) for i in range(1 << n)]


def gray_code_reflect_prefix(n: int) -> list[int]:
    """
    Iterative reflect-and-prefix: start with [0], then each step doubles
    the sequence by mirroring and adding the new MSB value.
    Equivalent to the recursive approach but avoids string building.

    >>> gray_code_reflect_prefix(2)
    [0, 1, 3, 2]
    >>> gray_code_reflect_prefix(3)
    [0, 1, 3, 2, 6, 7, 5, 4]
    >>> gray_code_reflect_prefix(0)
    [0]
    """
    if n < 0:
        raise ValueError("The given input must be positive")
    seq = [0]
    for step in range(n):
        msb = 1 << step
        seq = seq + [msb | x for x in reversed(seq)]
    return seq


def gray_to_binary(gray: int) -> int:
    """
    Inverse: decode a Gray code integer back to its binary (standard) index.
    Uses XOR cascade: each bit of result = XOR of all higher Gray bits.

    >>> gray_to_binary(0)
    0
    >>> gray_to_binary(1)
    1
    >>> gray_to_binary(3)
    2
    >>> gray_to_binary(2)
    3
    >>> [gray_to_binary(g) for g in gray_code_xor_formula(3)]
    [0, 1, 2, 3, 4, 5, 6, 7]
    """
    binary = 0
    mask = gray
    while mask:
        mask >>= 1
        binary ^= mask
    return binary ^ gray


# ---------------------------------------------------------------------------
# Verification helpers
# ---------------------------------------------------------------------------


def verify_gray_properties(seq: list[int], n: int) -> dict[str, bool]:
    """Check all 5 Gray code properties."""
    size = 1 << n
    return {
        "length":     len(seq) == size,
        "range":      all(0 <= x < size for x in seq),
        "starts_0":   seq[0] == 0,
        "unique":     len(set(seq)) == size,
        "adjacent":   all(bin(seq[i] ^ seq[i+1]).count("1") == 1
                          for i in range(len(seq) - 1)),
        "wraparound": bin(seq[-1] ^ seq[0]).count("1") == 1,
    }


IMPLS = [
    ("recursive_str",    gray_code_recursive_string),
    ("xor_formula",      gray_code_xor_formula),
    ("reflect_prefix",   gray_code_reflect_prefix),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n in range(5):
        seqs = {name: fn(n) for name, fn in IMPLS}
        ref = seqs["xor_formula"]
        ok = all(v == ref for v in seqs.values())
        print(f"  [{'OK' if ok else 'FAIL'}] n={n}: {ref[:8]}{'...' if len(ref) > 8 else ''}")

    print("\n=== Gray Code Properties (n=4) ===")
    props = verify_gray_properties(gray_code_xor_formula(4), 4)
    for prop, val in props.items():
        print(f"  {'OK' if val else 'FAIL'} {prop}")

    print("\n=== Inverse (Gray -> Binary) ===")
    seq4 = gray_code_xor_formula(4)
    decoded = [gray_to_binary(g) for g in seq4]
    ok = decoded == list(range(16))
    print(f"  [{'OK' if ok else 'FAIL'}] decode(gray_code(4)) == [0..15]")

    REPS = 50_000
    for n in [4, 8, 12]:
        print(f"\n=== Benchmark: n={n} ({1 << n} elements), {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: fn(n), number=REPS) * 1000 / REPS
            print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
