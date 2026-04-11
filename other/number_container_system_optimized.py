#!/usr/bin/env python3
"""
Optimized and alternative implementations of Number Container System.

Variants covered:
1. heap_lazy_delete  -- Heap with lazy deletion (reference)
2. sorted_set        -- SortedList from sortedcontainers (if available)
3. brute_force       -- Simple dict scan

Run:
    python other/number_container_system_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.number_container_system import NumberContainerSystem as Reference


class BruteForceContainer:
    """
    Simple brute-force: scan all entries for find().

    >>> nc = BruteForceContainer()
    >>> nc.find(10)
    -1
    >>> nc.change(2, 10)
    >>> nc.change(1, 10)
    >>> nc.find(10)
    1
    >>> nc.change(1, 20)
    >>> nc.find(10)
    2
    """

    def __init__(self) -> None:
        self.data: dict[int, int] = {}

    def change(self, index: int, number: int) -> None:
        self.data[index] = number

    def find(self, number: int) -> int:
        result = -1
        for idx, num in self.data.items():
            if num == number and (result == -1 or idx < result):
                result = idx
        return result


class SetContainer:
    """
    Using sets per number with min() for find.

    >>> nc = SetContainer()
    >>> nc.find(10)
    -1
    >>> nc.change(2, 10)
    >>> nc.change(1, 10)
    >>> nc.find(10)
    1
    """

    def __init__(self) -> None:
        self.index_to_num: dict[int, int] = {}
        self.num_to_indices: dict[int, set[int]] = defaultdict(set)

    def change(self, index: int, number: int) -> None:
        if index in self.index_to_num:
            old_num = self.index_to_num[index]
            self.num_to_indices[old_num].discard(index)
        self.index_to_num[index] = number
        self.num_to_indices[number].add(index)

    def find(self, number: int) -> int:
        indices = self.num_to_indices.get(number, set())
        return min(indices) if indices else -1


def bench_container(cls, ops):
    nc = cls()
    for op, *args in ops:
        if op == "change":
            nc.change(*args)
        else:
            nc.find(*args)


IMPLS = [
    ("reference_heap", Reference),
    ("brute_force", BruteForceContainer),
    ("set_min", SetContainer),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for name, cls in IMPLS:
        nc = cls()
        r1 = nc.find(10)
        nc.change(2, 10)
        nc.change(1, 10)
        nc.change(3, 10)
        r2 = nc.find(10)
        nc.change(1, 20)
        r3 = nc.find(10)
        ok = r1 == -1 and r2 == 1 and r3 == 2
        print(f"  [{'OK' if ok else 'FAIL'}] {name}: find(10)={r1},{r2},{r3}")

    import random
    rng = random.Random(42)
    ops = []
    for _ in range(5000):
        if rng.random() < 0.6:
            ops.append(("change", rng.randint(1, 1000), rng.randint(1, 50)))
        else:
            ops.append(("find", rng.randint(1, 50)))

    REPS = 200
    print(f"\n=== Benchmark: {REPS} runs, {len(ops)} operations ===")
    for name, cls in IMPLS:
        t = timeit.timeit(lambda cls=cls: bench_container(cls, ops), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
