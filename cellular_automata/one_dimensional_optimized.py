"""
One-Dimensional Cellular Automaton - Optimized Variants with Benchmark
https://mathworld.wolfram.com/ElementaryCellularAutomaton.html

Variant 1: list_based      - Pure Python per-cell loop
Variant 2: numpy_lookup    - NumPy with vectorized bit-shift lookup
Variant 3: bitwise_packed  - Entire row packed as single integer (fastest)
"""

from __future__ import annotations

import time

import numpy as np


# ---- Variant 1: List-based ----
def run_list(rule_number: int, width: int, generations: int) -> list[list[int]]:
    """
    Pure Python list-based approach.

    >>> run_list(90, 7, 3)
    [[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1]]
    """
    rule = [int(c) for c in f"{rule_number:08b}"]
    cells = [[0] * width]
    cells[0][width // 2] = 1

    for _ in range(generations):
        prev = cells[-1]
        row = []
        for i in range(width):
            left = 0 if i == 0 else prev[i - 1]
            right = 0 if i == width - 1 else prev[i + 1]
            pattern = 7 - (left * 4 + prev[i] * 2 + right)
            row.append(rule[pattern])
        cells.append(row)
    return cells


# ---- Variant 2: NumPy lookup table ----
def run_numpy(rule_number: int, width: int, generations: int) -> list[list[int]]:
    """
    NumPy vectorized approach using bit-shift to compute lookup indices.

    >>> run_numpy(90, 7, 3)
    [[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1]]
    """
    # Build lookup: index 0..7 -> output bit
    lookup = np.array([(rule_number >> i) & 1 for i in range(8)], dtype=np.int8)

    row = np.zeros(width, dtype=np.int8)
    row[width // 2] = 1
    history = [row.tolist()]

    for _ in range(generations):
        # Compute 3-bit neighbourhood index for each cell
        left = np.roll(row, 1)
        left[0] = 0
        right = np.roll(row, -1)
        right[-1] = 0
        indices = left * 4 + row * 2 + right  # 0..7
        row = lookup[indices]
        history.append(row.tolist())
    return history


# ---- Variant 3: Bitwise packed integer ----
def run_bitwise(rule_number: int, width: int, generations: int) -> list[list[int]]:
    """
    Entire row stored as a single Python integer. Neighbourhood computed
    with bit shifts and masks.

    >>> run_bitwise(90, 7, 3)
    [[0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1]]
    """
    row = 1 << (width // 2)
    mask = (1 << width) - 1

    def int_to_list(val: int) -> list[int]:
        return [(val >> (width - 1 - i)) & 1 for i in range(width)]

    history = [int_to_list(row)]

    for _ in range(generations):
        new_row = 0
        for bit in range(width):
            # Extract 3-bit neighbourhood (MSB to LSB order)
            left = (row >> (bit + 1)) & 1 if bit + 1 < width else 0
            center = (row >> bit) & 1
            right = (row >> (bit - 1)) & 1 if bit > 0 else 0
            pattern = left * 4 + center * 2 + right
            if (rule_number >> pattern) & 1:
                new_row |= 1 << bit
        row = new_row & mask
        history.append(int_to_list(row))
    return history


# ---- Benchmark ----
def benchmark(width: int = 1001, generations: int = 500, rule: int = 30) -> None:
    """Run all three variants and compare performance."""
    print(f"1D Cellular Automaton Benchmark (Rule {rule})")
    print(f"Width: {width}, Generations: {generations}")
    print("=" * 55)

    start = time.perf_counter()
    r1 = run_list(rule, width, generations)
    t1 = time.perf_counter() - start

    start = time.perf_counter()
    r2 = run_numpy(rule, width, generations)
    t2 = time.perf_counter() - start

    start = time.perf_counter()
    r3 = run_bitwise(rule, width, generations)
    t3 = time.perf_counter() - start

    # Verify all produce same results
    assert r1 == r2, "Mismatch: list vs numpy"
    assert r1 == r3, "Mismatch: list vs bitwise"

    print(f"{'Variant':<25} {'Time (s)':<12} {'Speedup'}")
    print("-" * 55)
    print(f"{'1. list_based':<25} {t1:<12.4f}")
    print(f"{'2. numpy_lookup':<25} {t2:<12.4f} {t1/t2:.1f}x")
    print(f"{'3. bitwise_packed':<25} {t3:<12.4f} {t1/t3:.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
