"""
Remove-digit variants + benchmark.

1. brute_force     - try every occurrence, keep max (lexicographic on equal length)
2. greedy_left     - single pass: remove d at position where s[i+1] > s[i]
                     falls back to last occurrence
3. regex_split     - split on digit, test concatenations (illustrative)
"""
from __future__ import annotations

import re
import time


def brute_force(s: str, d: str) -> str:
    best = ""
    for i, c in enumerate(s):
        if c == d:
            cand = s[:i] + s[i + 1 :]
            if cand > best:
                best = cand
    return best


def greedy_left(s: str, d: str) -> str:
    last = -1
    for i, c in enumerate(s):
        if c == d:
            last = i
            if i + 1 < len(s) and s[i + 1] > d:
                return s[:i] + s[i + 1 :]
    return s[:last] + s[last + 1 :]


def regex_split(s: str, d: str) -> str:
    positions = [m.start() for m in re.finditer(re.escape(d), s)]
    best = ""
    for i in positions:
        cand = s[:i] + s[i + 1 :]
        if cand > best:
            best = cand
    return best


def benchmark() -> None:
    import random

    rng = random.Random(0)
    s = "".join(rng.choice("0123456789") for _ in range(1000))
    d = "5"
    print(f"{'fn':<14}{'ms':>12}")
    for fn in (brute_force, greedy_left, regex_split):
        t = time.perf_counter()
        for _ in range(1000):
            fn(s, d)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<14}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
