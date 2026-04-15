"""
Sock merchant variants + benchmark.

1. counter_div2   - Counter then sum of count//2
2. set_sweep      - single pass toggling in a set
3. sort_then_pair - sort, count consecutive equal pairs
"""
from __future__ import annotations

import time
from collections import Counter


def counter_div2(socks):
    return sum(c // 2 for c in Counter(socks).values())


def set_sweep(socks):
    seen = set()
    pairs = 0
    for s in socks:
        if s in seen:
            seen.discard(s)
            pairs += 1
        else:
            seen.add(s)
    return pairs


def sort_then_pair(socks):
    arr = sorted(socks)
    pairs = 0
    i = 0
    while i < len(arr) - 1:
        if arr[i] == arr[i + 1]:
            pairs += 1
            i += 2
        else:
            i += 1
    return pairs


def benchmark() -> None:
    import random

    rng = random.Random(0)
    data = [rng.randrange(0, 100) for _ in range(10_000)]
    print(f"{'fn':<16}{'ms':>12}")
    for fn in (counter_div2, set_sweep, sort_then_pair):
        t = time.perf_counter()
        for _ in range(1000):
            fn(data)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<16}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
