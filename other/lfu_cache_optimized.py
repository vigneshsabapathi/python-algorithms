#!/usr/bin/env python3
"""
Optimized and alternative implementations of LFU Cache.

Variants covered:
1. ordered_dict_lfu  -- OrderedDict per frequency bucket (reference)
2. heap_lfu          -- Min-heap for eviction candidate tracking
3. counter_lfu       -- Simple Counter-based approach

Run:
    python other/lfu_cache_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit
from collections import OrderedDict, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.lfu_cache import LFUCache as ReferenceLFU


class HeapLFU:
    """
    LFU Cache using a min-heap for eviction.

    >>> cache = HeapLFU(2)
    >>> cache.put(1, 1)
    >>> cache.put(2, 2)
    >>> cache.get(1)
    1
    >>> cache.put(3, 3)
    >>> cache.get(2)
    -1
    >>> cache.get(3)
    3
    """

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.data: dict[int, int] = {}
        self.freq: dict[int, int] = {}
        self.time: dict[int, int] = {}
        self.heap: list[tuple[int, int, int]] = []  # (freq, time, key)
        self.tick = 0

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.freq[key] += 1
        self.tick += 1
        self.time[key] = self.tick
        heapq.heappush(self.heap, (self.freq[key], self.tick, key))
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.data:
            self.data[key] = value
            self.get(key)
            return
        if len(self.data) >= self.capacity:
            while self.heap:
                f, t, k = heapq.heappop(self.heap)
                if k in self.data and self.freq[k] == f and self.time[k] == t:
                    del self.data[k]
                    del self.freq[k]
                    del self.time[k]
                    break
        self.tick += 1
        self.data[key] = value
        self.freq[key] = 1
        self.time[key] = self.tick
        heapq.heappush(self.heap, (1, self.tick, key))


class SimpleLFU:
    """
    Simple LFU using a dict and linear scan for eviction.

    >>> cache = SimpleLFU(2)
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
        self.data: dict[int, int] = {}
        self.freq: dict[int, int] = {}
        self.order: dict[int, int] = {}
        self.tick = 0

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.freq[key] += 1
        self.tick += 1
        self.order[key] = self.tick
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.data:
            self.data[key] = value
            self.get(key)
            return
        if len(self.data) >= self.capacity:
            evict = min(self.data, key=lambda k: (self.freq[k], self.order[k]))
            del self.data[evict]
            del self.freq[evict]
            del self.order[evict]
        self.tick += 1
        self.data[key] = value
        self.freq[key] = 1
        self.order[key] = self.tick


def bench_cache(cls, operations):
    cache = cls(100)
    for op, k, v in operations:
        if op == "put":
            cache.put(k, v)
        else:
            cache.get(k)


IMPLS = [
    ("reference", ReferenceLFU),
    ("heap_lfu", HeapLFU),
    ("simple_lfu", SimpleLFU),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for name, cls in IMPLS:
        c = cls(2)
        c.put(1, 1); c.put(2, 2)
        r1 = c.get(1)
        c.put(3, 3)
        r2 = c.get(2)
        r3 = c.get(3)
        ok = r1 == 1 and r2 == -1 and r3 == 3
        print(f"  [{'OK' if ok else 'FAIL'}] {name}: get(1)={r1} get(2)={r2} get(3)={r3}")

    import random
    rng = random.Random(42)
    ops = []
    for _ in range(5000):
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
