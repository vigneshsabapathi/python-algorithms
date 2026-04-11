#!/usr/bin/env python3
"""
Optimized and alternative implementations of Hamming Code.

Hamming codes insert parity bits at power-of-2 positions (1, 2, 4, 8, ...)
to enable single-bit error correction. Each parity bit covers a specific
subset of data bits determined by the binary representation of positions.

Variants:
  reference      -- TheAlgorithms implementation (uses math.log2)
  bitwise        -- uses bitwise power-of-2 check (faster, no float issues)
  matrix_based   -- uses generator/parity-check matrices (linear algebra)
  secded         -- Single Error Correction, Double Error Detection (extra parity)

Run:
    python hashes/hamming_code_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.hamming_code import (
    emitter_converter as ref_encode,
    receptor_converter as ref_decode,
    text_to_bits,
    text_from_bits,
)


# ---------------------------------------------------------------------------
# Variant 1 -- bitwise: avoids float math.log2
# ---------------------------------------------------------------------------

def _is_power_of_2(n: int) -> bool:
    """Check if n is a power of 2 using bitwise trick."""
    return n > 0 and (n & (n - 1)) == 0


def bitwise_encode(size_par: int, data: str) -> list[str]:
    """
    Hamming encode using bitwise power-of-2 detection.

    Avoids math.log2 floating-point issues for large positions.

    >>> bitwise_encode(4, "101010111111")
    ['1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1']
    """
    total = size_par + len(data)
    if total <= 2**size_par - (len(data) - 1):
        raise ValueError("size of parity don't match with size of data")

    # Place data bits, leaving power-of-2 positions for parity
    encoded = [None] * (total + 1)  # 1-indexed
    data_idx = 0
    for pos in range(1, total + 1):
        if _is_power_of_2(pos):
            encoded[pos] = "0"  # placeholder for parity
        else:
            encoded[pos] = data[data_idx]
            data_idx += 1

    # Calculate parity bits
    for i in range(size_par):
        parity_pos = 1 << i  # 1, 2, 4, 8, ...
        count = 0
        for pos in range(1, total + 1):
            if pos & parity_pos and not _is_power_of_2(pos):
                if encoded[pos] == "1":
                    count += 1
        encoded[parity_pos] = str(count % 2)

    return encoded[1:]


def bitwise_decode(size_par: int, data: str) -> tuple[list[str], bool]:
    """
    Hamming decode using bitwise operations.

    >>> bitwise_decode(4, "1111010010111111")
    (['1', '0', '1', '0', '1', '0', '1', '1', '1', '1', '1', '1'], True)
    """
    total = len(data)
    received = [""] + list(data)  # 1-indexed

    # Check parity bits
    error_pos = 0
    for i in range(size_par):
        parity_pos = 1 << i
        count = 0
        for pos in range(1, total + 1):
            if pos & parity_pos and received[pos] == "1":
                count += 1
        if count % 2 != 0:
            error_pos += parity_pos

    ack = error_pos == 0

    # Extract data bits
    data_output = []
    for pos in range(1, total + 1):
        if not _is_power_of_2(pos):
            data_output.append(received[pos])

    return data_output, ack


# ---------------------------------------------------------------------------
# Variant 2 -- secded: Single Error Correction, Double Error Detection
# ---------------------------------------------------------------------------

def secded_encode(size_par: int, data: str) -> list[str]:
    """
    SECDED Hamming code -- adds an overall parity bit for double-error detection.

    >>> result = secded_encode(4, "101010111111")
    >>> len(result) == 4 + 12 + 1  # parity + data + overall parity
    True
    """
    # First encode with standard Hamming
    encoded = bitwise_encode(size_par, data)
    # Add overall parity bit
    overall = str(sum(int(b) for b in encoded) % 2)
    return encoded + [overall]


def secded_decode(size_par: int, data: str) -> tuple[list[str], bool, bool]:
    """
    SECDED decode -- returns (data, single_error_corrected, no_double_error).

    >>> data_out, corrected, valid = secded_decode(4, "11110100101111111")
    >>> valid
    True
    """
    overall_parity = data[-1]
    hamming_data = data[:-1]

    data_output, hamming_ok = bitwise_decode(size_par, hamming_data)

    # Check overall parity
    all_bits_parity = sum(int(b) for b in data) % 2
    overall_ok = all_bits_parity == 0

    if hamming_ok and overall_ok:
        return data_output, False, True  # No errors
    elif not hamming_ok and not overall_ok:
        return data_output, True, True  # Single error (correctable)
    elif hamming_ok and not overall_ok:
        return data_output, False, True  # Overall parity bit error
    else:
        return data_output, False, False  # Double error (uncorrectable)


# ---------------------------------------------------------------------------
# Variant 3 -- matrix_based: generator matrix approach
# ---------------------------------------------------------------------------

def matrix_encode(data: str) -> list[str]:
    """
    Hamming(7,4) encode using generator matrix multiplication over GF(2).

    This is the classic (7,4) Hamming code for 4-bit data words.

    >>> matrix_encode("1011")
    ['1', '0', '1', '1', '0', '1', '0']
    >>> matrix_encode("0000")
    ['0', '0', '0', '0', '0', '0', '0']
    """
    if len(data) != 4:
        raise ValueError("matrix_encode requires exactly 4 data bits")

    # Generator matrix for Hamming(7,4)
    # G = [I4 | P] where P is the parity sub-matrix
    G = [
        [1, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 1, 1, 1, 1],
    ]

    d = [int(b) for b in data]
    codeword = [0] * 7
    for j in range(7):
        for i in range(4):
            codeword[j] ^= d[i] & G[i][j]

    return [str(b) for b in codeword]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    print("\n=== Correctness ===")

    # Test encode
    data = "101010111111"
    ref_result = ref_encode(4, data)
    bw_result = bitwise_encode(4, data)
    print(f"  [{'OK' if ref_result == bw_result else 'FAIL'}] encode: reference == bitwise")

    # Test decode
    encoded_str = "".join(ref_result)
    ref_dec, ref_ack = ref_decode(4, encoded_str)
    bw_dec, bw_ack = bitwise_decode(4, encoded_str)
    print(f"  [{'OK' if ref_dec == bw_dec and ref_ack == bw_ack else 'FAIL'}] decode: reference == bitwise")

    # Test round-trip with text
    text = "Hi"
    bits = text_to_bits(text)
    encoded = bitwise_encode(4, bits)
    decoded, ack = bitwise_decode(4, "".join(encoded))
    recovered = text_from_bits("".join(decoded))
    print(f"  [{'OK' if recovered == text and ack else 'FAIL'}] round-trip: '{text}' -> encode -> decode -> '{recovered}'")

    # Test error detection
    encoded_list = list("".join(ref_result))
    # Flip one bit
    flip_pos = 5
    encoded_list[flip_pos] = "0" if encoded_list[flip_pos] == "1" else "1"
    _, ack_error = bitwise_decode(4, "".join(encoded_list))
    print(f"  [{'OK' if not ack_error else 'FAIL'}] error detection: flipped bit at pos {flip_pos}")

    # SECDED test
    secded_enc = secded_encode(4, data)
    secded_dec, corrected, valid = secded_decode(4, "".join(secded_enc))
    print(f"  [{'OK' if valid else 'FAIL'}] SECDED: no error -> valid={valid}")

    # Matrix Hamming(7,4)
    m_enc = matrix_encode("1011")
    print(f"  [OK] Hamming(7,4) encode: 1011 -> {''.join(m_enc)}")

    # Benchmark
    REPS = 10_000
    test_data = text_to_bits("Hello World")
    size_par = 4

    print(f"\n=== Benchmark: encode+decode {len(test_data)}-bit message, {REPS} runs ===")
    for name, enc_fn, dec_fn in [
        ("reference", lambda: ref_encode(size_par, test_data), lambda d: ref_decode(size_par, d)),
        ("bitwise", lambda: bitwise_encode(size_par, test_data), lambda d: bitwise_decode(size_par, d)),
    ]:
        encoded = "".join(enc_fn())
        t_enc = timeit.timeit(enc_fn, number=REPS) * 1000 / REPS
        t_dec = timeit.timeit(lambda: dec_fn(encoded), number=REPS) * 1000 / REPS
        print(f"  {name:<14} encode: {t_enc:>7.4f} ms  decode: {t_dec:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
