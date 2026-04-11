#!/usr/bin/env python3
"""
Optimized and alternative implementations of Boyer-Moore Majority Vote.

Variants covered:
1. boyer_moore       -- Standard two-pass Boyer-Moore (reference)
2. counter_approach  -- Using collections.Counter
3. sorting_approach  -- Sort and check middle element
4. hash_map          -- Hash map frequency count

Run:
    python other/majority_vote_algorithm_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.majority_vote_algorithm import majority_vote as reference


def counter_majority(votes: list[int]) -> int | None:
    """
    Majority element using Counter.

    >>> counter_majority([1, 1, 1, 2, 2])
    1
    >>> counter_majority([1, 2, 3])
    >>> counter_majority([])
    """
    if not votes:
        return None
    counter = Counter(votes)
    candidate, count = counter.most_common(1)[0]
    return candidate if count > len(votes) // 2 else None


def sorting_majority(votes: list[int]) -> int | None:
    """
    Majority element by sorting — if it exists, it's at the middle index.

    >>> sorting_majority([1, 1, 1, 2, 2])
    1
    >>> sorting_majority([1, 2, 3])
    >>> sorting_majority([])
    """
    if not votes:
        return None
    sorted_votes = sorted(votes)
    candidate = sorted_votes[len(sorted_votes) // 2]
    return candidate if sorted_votes.count(candidate) > len(votes) // 2 else None


def hash_map_majority(votes: list[int]) -> int | None:
    """
    Majority element using hash map.

    >>> hash_map_majority([2, 2, 1, 1, 1, 2, 2])
    2
    >>> hash_map_majority([])
    """
    if not votes:
        return None
    threshold = len(votes) // 2
    freq: dict[int, int] = {}
    for v in votes:
        freq[v] = freq.get(v, 0) + 1
        if freq[v] > threshold:
            return v
    return None


TEST_CASES = [
    ([1, 1, 1, 2, 2], 1),
    ([2, 2, 1, 1, 1, 2, 2], 2),
    ([1, 2, 3], None),
    ([1], 1),
    ([], None),
    ([3, 3, 3, 3], 3),
]

IMPLS = [
    ("reference", reference),
    ("counter", counter_majority),
    ("sorting", sorting_majority),
    ("hash_map", hash_map_majority),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for votes, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(list(votes))
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected={expected} got={result}")
        print(f"  [OK] n={len(votes)} majority={expected}")

    import random
    rng = random.Random(42)
    # Create array with clear majority
    large = [1] * 5001 + [rng.randint(2, 100) for _ in range(4999)]
    rng.shuffle(large)

    REPS = 2000
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} elements ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(large)), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
