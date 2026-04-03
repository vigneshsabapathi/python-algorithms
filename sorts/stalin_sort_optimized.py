"""Optimized and alternative implementations of Stalin Sort.

Stalin sort is a joke algorithm: it "sorts" by purging any element that is
smaller than the previous one. The result is the longest non-decreasing
PREFIX starting from the first element — not a full sort.

Variants:
1. Original (crashes on empty list)
2. Defensive (guards empty list, same logic)
3. Functional one-liner (itertools.accumulate comparison)
4. With purge counter (tracks how many elements were removed)
5. Longest Non-Decreasing Subsequence (keeps the most elements possible)
6. sorted() — for contrast: actually sorts all elements in O(n log n)

Key insight for interviews: variants 1-4 are O(n) but return a SHORTER list.
Variant 5 (LNDS) is the "correct" extension — O(n log n), keeps most elements.
"""

from __future__ import annotations
import itertools
import bisect
import time
import random


# ---------------------------------------------------------------------------
# 1. Original — crashes on empty input
# ---------------------------------------------------------------------------
def stalin_sort_original(sequence: list) -> list:
    """Original: O(n), crashes on empty list.

    >>> stalin_sort_original([4, 3, 5, 2, 1, 7])
    [4, 5, 7]
    >>> stalin_sort_original([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> stalin_sort_original([5, 4, 3, 2, 1])
    [5]
    """
    result = [sequence[0]]
    for element in sequence[1:]:
        if element >= result[-1]:
            result.append(element)
    return result


# ---------------------------------------------------------------------------
# 2. Defensive — handles empty list
# ---------------------------------------------------------------------------
def stalin_sort(sequence: list) -> list:
    """Defensive version: returns [] for empty input instead of crashing.

    >>> stalin_sort([4, 3, 5, 2, 1, 7])
    [4, 5, 7]
    >>> stalin_sort([])
    []
    >>> stalin_sort([42])
    [42]
    >>> stalin_sort([3, 3, 3])
    [3, 3, 3]
    """
    if not sequence:
        return []
    result = [sequence[0]]
    for element in sequence[1:]:
        if element >= result[-1]:
            result.append(element)
    return result


# ---------------------------------------------------------------------------
# 3. Functional one-liner using itertools.accumulate
#    accumulate(seq, max) yields running maximum; keep element if it equals
#    the running max up to that point (i.e. it didn't decrease)
# ---------------------------------------------------------------------------
def stalin_sort_functional(sequence: list) -> list:
    """One-liner: uses itertools.accumulate to track running maximum.

    >>> stalin_sort_functional([4, 3, 5, 2, 1, 7])
    [4, 5, 7]
    >>> stalin_sort_functional([])
    []
    >>> stalin_sort_functional([1, 2, 3])
    [1, 2, 3]
    """
    if not sequence:
        return []
    running_max = list(itertools.accumulate(sequence, max))
    # Keep element only if it matches the running max at that position
    # (meaning it didn't trigger a new max by going down)
    prev_max = [None] + running_max[:-1]  # running max BEFORE this element
    return [
        x for x, pm in zip(sequence, prev_max)
        if pm is None or x >= pm
    ]


# ---------------------------------------------------------------------------
# 4. With purge counter — useful for diagnostics / interview discussion
# ---------------------------------------------------------------------------
def stalin_sort_counted(sequence: list) -> tuple[list, int]:
    """Returns (sorted result, number of purged elements).

    >>> stalin_sort_counted([4, 3, 5, 2, 1, 7])
    ([4, 5, 7], 3)
    >>> stalin_sort_counted([1, 2, 3])
    ([1, 2, 3], 0)
    >>> stalin_sort_counted([])
    ([], 0)
    """
    if not sequence:
        return [], 0
    result = [sequence[0]]
    purged = 0
    for element in sequence[1:]:
        if element >= result[-1]:
            result.append(element)
        else:
            purged += 1
    return result, purged


# ---------------------------------------------------------------------------
# 5. Longest Non-Decreasing Subsequence (LNDS)
#    The "fair" extension: keeps the MOST elements possible (not just a prefix)
#    Uses patience sorting / binary search — O(n log n)
#    This is the correct answer to "sort while discarding fewest elements"
# ---------------------------------------------------------------------------
def longest_nondecreasing_subsequence(sequence: list) -> list:
    """Returns the longest non-decreasing subsequence (not just the prefix).
    Discards the fewest possible elements to produce a sorted result.
    O(n log n) via patience sort + binary search.

    >>> longest_nondecreasing_subsequence([4, 3, 5, 2, 1, 7])
    [3, 5, 7]
    >>> longest_nondecreasing_subsequence([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> longest_nondecreasing_subsequence([5, 4, 3, 2, 1])
    [1]
    >>> longest_nondecreasing_subsequence([4, 5, 5, 2, 3])
    [4, 5, 5]
    >>> longest_nondecreasing_subsequence([])
    []
    """
    if not sequence:
        return []
    # tails[i] = smallest tail of all non-decreasing subsequences of length i+1
    tails: list = []
    # parent[i] = index of predecessor of sequence[i] in the LNDS
    parent = [-1] * len(sequence)
    # index into tails that each element extends
    tail_idx = [-1] * len(sequence)

    for i, x in enumerate(sequence):
        # bisect_right: allow equal elements (non-decreasing, not strictly increasing)
        pos = bisect.bisect_right(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
        tail_idx[i] = pos
        # Track predecessor for reconstruction
        if pos > 0:
            # Find the most recent element assigned to position pos-1
            for j in range(i - 1, -1, -1):
                if tail_idx[j] == pos - 1 and sequence[j] <= x:
                    parent[i] = j
                    break

    # Reconstruct: find the last element assigned to the longest position
    length = len(tails)
    idx = -1
    for i in range(len(sequence) - 1, -1, -1):
        if tail_idx[i] == length - 1:
            idx = i
            break

    result = []
    while idx != -1:
        result.append(sequence[idx])
        idx = parent[idx]
    return result[::-1]


# ---------------------------------------------------------------------------
# 6. sorted() — for contrast (actually sorts ALL elements)
# ---------------------------------------------------------------------------
def sort_builtin(sequence: list) -> list:
    """Python sorted() — keeps all elements, O(n log n).

    >>> sort_builtin([4, 3, 5, 2, 1, 7])
    [1, 2, 3, 4, 5, 7]
    >>> sort_builtin([])
    []
    """
    return sorted(sequence)


# ---------------------------------------------------------------------------
# Benchmark + element retention analysis
# ---------------------------------------------------------------------------
def benchmark() -> None:
    print("Element retention analysis (random data, 10 unique values):")
    print(f"  {'n':>6}  {'kept (stalin)':>14}  {'kept (LNDS)':>12}  {'purged%':>8}")
    for n in [20, 50, 100, 500, 1000]:
        data = [random.randint(1, 10) for _ in range(n)]
        kept_stalin = len(stalin_sort(data))
        kept_lnds = len(longest_nondecreasing_subsequence(data))
        pct = (n - kept_stalin) / n * 100
        print(f"  {n:>6}  {kept_stalin:>14}  {kept_lnds:>12}  {pct:>7.1f}%")

    print("\nSpeed benchmark (random integers, best of 3 runs):")
    variants = [
        ("stalin (defensive) ", stalin_sort),
        ("stalin (functional)", stalin_sort_functional),
        ("LNDS               ", longest_nondecreasing_subsequence),
        ("sorted()           ", sort_builtin),
    ]
    for n in [1_000, 10_000, 100_000]:
        data = [random.randint(0, n) for _ in range(n)]
        print(f"  n={n:,}")
        for name, fn in variants:
            best = float("inf")
            for _ in range(3):
                t0 = time.perf_counter()
                fn(list(data))
                best = min(best, time.perf_counter() - t0)
            print(f"    {name}: {best * 1000:8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("All doctests passed.\n")
    benchmark()
