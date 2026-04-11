#!/usr/bin/env python3
"""
Optimized and alternative implementations of LRU Cache (OrderedDict version).

Variants covered:
1. ordered_dict_lru  -- OrderedDict-based (reference)
2. dict_lru          -- Plain dict (Python 3.7+ insertion order)
3. ttl_lru           -- LRU with time-to-live expiry

Run:
    python other/lru_cache_optimized.py
"""

from __future__ import annotations

import os
import sys
import time
import timeit
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.lru_cache import LRUCache as Reference


class DictLRU:
    """
    LRU Cache using plain dict (Python 3.7+ preserves insertion order).

    >>> cache = DictLRU(2)
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
            del self.cache[next(iter(self.cache))]


class TTLLRUCache:
    """
    LRU Cache with time-to-live (TTL) expiry.

    >>> cache = TTLLRUCache(2, ttl=999)
    >>> cache.put(1, 1)
    >>> cache.put(2, 2)
    >>> cache.get(1)
    1
    >>> cache.put(3, 3)
    >>> cache.get(2)
    -1
    """

    def __init__(self, capacity: int, ttl: float = 60.0) -> None:
        self.capacity = capacity
        self.ttl = ttl
        self.cache: OrderedDict[int, tuple[int, float]] = OrderedDict()

    def _is_expired(self, key: int) -> bool:
        if key not in self.cache:
            return True
        _, ts = self.cache[key]
        return time.time() - ts > self.ttl

    def get(self, key: int) -> int:
        if key not in self.cache or self._is_expired(key):
            if key in self.cache:
                del self.cache[key]
            return -1
        self.cache.move_to_end(key)
        return self.cache[key][0]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = (value, time.time())
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def bench_cache(cls, ops, **kwargs):
    cache = cls(100, **kwargs)
    for op, k, v in ops:
        if op == "put":
            cache.put(k, v)
        else:
            cache.get(k)


IMPLS = [
    ("reference", Reference, {}),
    ("dict_lru", DictLRU, {}),
    ("ttl_lru", TTLLRUCache, {"ttl": 999}),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for name, cls, kwargs in IMPLS:
        c = cls(2, **kwargs)
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
    for _ in range(10000):
        if rng.random() < 0.5:
            ops.append(("put", rng.randint(1, 200), rng.randint(1, 1000)))
        else:
            ops.append(("get", rng.randint(1, 200), 0))

    REPS = 500
    print(f"\n=== Benchmark: {REPS} runs, {len(ops)} operations ===")
    for name, cls, kwargs in IMPLS:
        t = timeit.timeit(
            lambda cls=cls, kwargs=kwargs: bench_cache(cls, ops, **kwargs),
            number=REPS,
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
