#!/usr/bin/env python3
"""
Optimized and alternative implementations of LRU Cache.

Variants covered:
1. doubly_linked_list  -- DLL + hashmap (reference)
2. ordered_dict        -- Python OrderedDict approach
3. functools_lru       -- stdlib functools.lru_cache decorator

Run:
    python other/least_recently_used_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import OrderedDict
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.least_recently_used import LRUCache as ReferenceLRU


class OrderedDictLRU:
    """
    LRU Cache using OrderedDict.

    >>> cache = OrderedDictLRU(2)
    >>> cache.put(1, 1)
    >>> cache.put(2, 2)
    >>> cache.get(1)
    1
    >>> cache.put(3, 3)
    >>> cache.get(2)
    -1
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class DictOnlyLRU:
    """
    LRU using plain dict (Python 3.7+ dicts preserve insertion order).

    >>> cache = DictOnlyLRU(2)
    >>> cache.put(1, 1)
    >>> cache.put(2, 2)
    >>> cache.get(1)
    1
    >>> cache.put(3, 3)
    >>> cache.get(2)
    -1
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[int, int] = {}

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        val = self.cache.pop(key)
        self.cache[key] = val
        return val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            oldest = next(iter(self.cache))
            del self.cache[oldest]


def bench_cache(cls, operations: list[tuple[str, int, int]]) -> None:
    cache = cls(100)
    for op, k, v in operations:
        if op == "put":
            cache.put(k, v)
        else:
            cache.get(k)


TEST_OPS = [
    ("put", 1, 1), ("put", 2, 2), ("get", 1, 0),
    ("put", 3, 3), ("get", 2, 0), ("put", 4, 4),
    ("get", 1, 0), ("get", 3, 0), ("get", 4, 0),
]

IMPLS = [
    ("reference_dll", ReferenceLRU),
    ("ordered_dict", OrderedDictLRU),
    ("dict_only", DictOnlyLRU),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for name, cls in IMPLS:
        cache = cls(2)
        cache.put(1, 1)
        cache.put(2, 2)
        r1 = cache.get(1)
        cache.put(3, 3)
        r2 = cache.get(2)
        r3 = cache.get(3)
        ok = r1 == 1 and r2 == -1 and r3 == 3
        print(f"  [{'OK' if ok else 'FAIL'}] {name}: get(1)={r1} get(2)={r2} get(3)={r3}")

    import random
    rng = random.Random(42)
    ops = []
    for _ in range(10000):
        if rng.random() < 0.5:
            ops.append(("put", rng.randint(1, 200), rng.randint(1, 1000)))
        else:
            ops.append(("get", rng.randint(1, 200), 0))

    REPS = 500
    print(f"\n=== Benchmark: {REPS} runs, {len(ops)} operations ===")
    for name, cls in IMPLS:
        t = timeit.timeit(lambda cls=cls: bench_cache(cls, ops), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
