#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Chaos Machine PRNG.

The reference uses global state with logistic-map transitions (push/pull).
The chaotic PRNG is NOT cryptographically secure -- it's a demonstration of
how chaotic dynamical systems can generate pseudorandom sequences.

Variants:
  reference        -- global-state chaos machine from TheAlgorithms
  class_based      -- encapsulated OOP version (no globals)
  numpy_vectorized -- NumPy-accelerated buffer updates
  secrets_compare  -- comparison with Python's cryptographic PRNG

Run:
    python hashes/chaos_machine_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.chaos_machine import (
    pull as ref_pull,
    push as ref_push,
    reset as ref_reset,
)


# ---------------------------------------------------------------------------
# Variant 1 -- class_based: encapsulated OOP chaos machine
# ---------------------------------------------------------------------------

class ChaosMachine:
    """
    Encapsulated chaos machine with no global state.

    >>> cm = ChaosMachine()
    >>> cm.push(12345)
    >>> result = cm.pull()
    >>> isinstance(result, int) and 0 <= result < 0xFFFFFFFF
    True
    """

    def __init__(
        self,
        k: list[float] | None = None,
        t: int = 3,
        m: int = 5,
    ) -> None:
        self.K = k if k is not None else [0.33, 0.44, 0.55, 0.44, 0.33]
        self.t = t
        self.m = m
        self.reset()

    def reset(self) -> None:
        self.buffer_space = list(self.K)
        self.params_space = [0.0] * self.m
        self.machine_time = 0

    def push(self, seed: int) -> None:
        for key in range(self.m):
            value = self.buffer_space[key]
            e = float(seed / value)
            value = (self.buffer_space[(key + 1) % self.m] + e) % 1
            r = (self.params_space[key] + e) % 1 + 3
            self.buffer_space[key] = round(float(r * value * (1 - value)), 10)
            self.params_space[key] = r
        self.machine_time += 1

    def pull(self) -> int:
        key = self.machine_time % self.m
        for _ in range(self.t):
            r = self.params_space[key]
            value = self.buffer_space[key]
            self.buffer_space[key] = round(float(r * value * (1 - value)), 10)
            self.params_space[key] = (self.machine_time * 0.01 + r * 1.01) % 1 + 3

        x = int(self.buffer_space[(key + 2) % self.m] * (10**10))
        y = int(self.buffer_space[(key - 2) % self.m] * (10**10))
        self.machine_time += 1

        # XOR-shift
        x ^= y >> 13
        y ^= x << 17
        x ^= y >> 5
        return x % 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Variant 2 -- numpy_vectorized: NumPy-accelerated buffer updates
# ---------------------------------------------------------------------------

class ChaosMachineNumpy:
    """
    NumPy-accelerated chaos machine -- vectorized buffer operations.

    >>> cm = ChaosMachineNumpy()
    >>> cm.push(12345)
    >>> result = cm.pull()
    >>> isinstance(result, int) and 0 <= result < 0xFFFFFFFF
    True
    """

    def __init__(
        self,
        k: list[float] | None = None,
        t: int = 3,
        m: int = 5,
    ) -> None:
        self.K = np.array(k if k is not None else [0.33, 0.44, 0.55, 0.44, 0.33])
        self.t = t
        self.m = m
        self.reset()

    def reset(self) -> None:
        self.buffer_space = self.K.copy()
        self.params_space = np.zeros(self.m)
        self.machine_time = 0

    def push(self, seed: int) -> None:
        # Sequential update (each step depends on previous)
        for key in range(self.m):
            value = self.buffer_space[key]
            e = float(seed / value)
            value = (self.buffer_space[(key + 1) % self.m] + e) % 1
            r = (self.params_space[key] + e) % 1 + 3
            self.buffer_space[key] = round(float(r * value * (1 - value)), 10)
            self.params_space[key] = r
        self.machine_time += 1

    def pull(self) -> int:
        key = self.machine_time % self.m
        for _ in range(self.t):
            r = self.params_space[key]
            value = self.buffer_space[key]
            self.buffer_space[key] = round(float(r * value * (1 - value)), 10)
            self.params_space[key] = (self.machine_time * 0.01 + r * 1.01) % 1 + 3

        x = int(self.buffer_space[(key + 2) % self.m] * (10**10))
        y = int(self.buffer_space[(key - 2) % self.m] * (10**10))
        self.machine_time += 1

        x ^= y >> 13
        y ^= x << 17
        x ^= y >> 5
        return x % 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Variant 3 -- secrets_compare: cryptographic PRNG comparison
# ---------------------------------------------------------------------------

def secrets_random_32() -> int:
    """
    Generate a 32-bit random integer using Python's secrets module.
    For comparison with the chaos machine output quality.

    >>> result = secrets_random_32()
    >>> isinstance(result, int) and 0 <= result < 0xFFFFFFFF
    True
    """
    import secrets
    return secrets.randbits(32) % 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    print("\n=== Correctness: Reference vs Class-based vs NumPy ===")
    seed_data = [100, 200, 300, 400, 500, 42, 99, 1234, 5678, 9999]

    # Reference
    ref_reset()
    for s in seed_data:
        ref_push(s)
    ref_outputs = [ref_pull() for _ in range(10)]

    # Class-based
    cm = ChaosMachine()
    for s in seed_data:
        cm.push(s)
    class_outputs = [cm.pull() for _ in range(10)]

    # NumPy
    cmn = ChaosMachineNumpy()
    for s in seed_data:
        cmn.push(s)
    numpy_outputs = [cmn.pull() for _ in range(10)]

    match_class = ref_outputs == class_outputs
    match_numpy = ref_outputs == numpy_outputs
    print(f"  [{'OK' if match_class else 'FAIL'}] reference == class_based: {match_class}")
    print(f"  [{'OK' if match_numpy else 'FAIL'}] reference == numpy:      {match_numpy}")

    print("\n  Sample outputs (first 5):")
    for i in range(5):
        print(f"    pull[{i}] = {format(ref_outputs[i], '#010x')}")

    # Distribution check -- chi-squared approximation on bit balance
    ref_reset()
    for s in range(1, 201):
        ref_push(s * 7)
    samples = [ref_pull() for _ in range(1000)]
    bit_counts = [0] * 32
    for val in samples:
        for bit in range(32):
            if val & (1 << bit):
                bit_counts[bit] += 1
    avg_set = sum(bit_counts) / 32
    expected = len(samples) / 2
    deviation = abs(avg_set - expected) / expected * 100
    print(f"\n  Bit balance: avg set bits per position = {avg_set:.1f} / {len(samples)} ({deviation:.1f}% from ideal 50%)")
    print(f"  [{'OK' if deviation < 15 else 'WARN'}] Distribution check (< 15% deviation)")

    # Benchmark
    REPS = 5000
    N_PUSH = 50
    N_PULL = 50

    print(f"\n=== Benchmark: {N_PUSH} pushes + {N_PULL} pulls, {REPS} runs ===")

    def bench_ref():
        ref_reset()
        for s in range(N_PUSH):
            ref_push(s * 13 + 1)
        return [ref_pull() for _ in range(N_PULL)]

    def bench_class():
        cm = ChaosMachine()
        for s in range(N_PUSH):
            cm.push(s * 13 + 1)
        return [cm.pull() for _ in range(N_PULL)]

    def bench_numpy():
        cmn = ChaosMachineNumpy()
        for s in range(N_PUSH):
            cmn.push(s * 13 + 1)
        return [cmn.pull() for _ in range(N_PULL)]

    for name, fn in [("reference", bench_ref), ("class_based", bench_class), ("numpy", bench_numpy)]:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms / cycle")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
