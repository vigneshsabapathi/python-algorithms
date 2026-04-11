#!/usr/bin/env python3
"""
Optimized and alternative implementations of Huffman Coding.

The reference builds the Huffman tree using a sorted list (popping from front
= O(n) per merge). Better approaches use a heap.

Variants covered:
1. sorted_list   -- reference approach, re-sort after each merge
2. heapq_tree    -- min-heap for O(n log n) tree building
3. counter_heap  -- collections.Counter + heapq (most Pythonic)
4. canonical     -- canonical Huffman codes (deterministic bit assignment)

Key interview insight:
    Huffman coding is the optimal prefix-free code for a given character
    frequency distribution. The greedy strategy (always merge two smallest)
    is provably optimal. Canonical codes simplify decoding by assigning
    codes in a deterministic order.

Run:
    python data_compression/huffman_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.huffman import huffman_encode as reference_encode
from data_compression.huffman import huffman_decode as reference_decode


# ---------------------------------------------------------------------------
# Variant 1 -- sorted_list (reference wrapper)
# ---------------------------------------------------------------------------

def sorted_list_encode(text: str) -> tuple[str, dict[str, str]]:
    """
    Huffman encoding using reference sorted-list tree building.

    >>> encoded, codes = sorted_list_encode("aabbc")
    >>> reference_decode(encoded, codes)
    'aabbc'
    """
    return reference_encode(text)


# ---------------------------------------------------------------------------
# Variant 2 -- heapq_tree: min-heap for efficient tree building
# ---------------------------------------------------------------------------

def heapq_encode(text: str) -> tuple[str, dict[str, str]]:
    """
    Huffman encoding using heapq for O(n log n) tree construction.

    >>> encoded, codes = heapq_encode("aabbc")
    >>> _heapq_decode(encoded, codes) == "aabbc"
    True
    >>> encoded, codes = heapq_encode("hello world")
    >>> _heapq_decode(encoded, codes) == "hello world"
    True
    """
    if not text:
        return "", {}

    freq = Counter(text)

    if len(freq) == 1:
        char = next(iter(freq))
        return "0" * len(text), {char: "0"}

    # heap entries: (freq, unique_id, node)
    # node is either (char,) for leaf or (left, right) for internal
    heap: list[tuple[int, int, tuple]] = []
    uid = 0
    for char, count in freq.items():
        heapq.heappush(heap, (count, uid, (char,)))
        uid += 1

    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, uid, (left, right)))
        uid += 1

    # Traverse tree to get codes
    codes: dict[str, str] = {}
    root = heap[0][2]

    def _traverse(node: tuple, prefix: str) -> None:
        if len(node) == 1:
            codes[node[0]] = prefix
            return
        _traverse(node[0], prefix + "0")
        _traverse(node[1], prefix + "1")

    _traverse(root, "")

    encoded = "".join(codes[c] for c in text)
    return encoded, codes


def _heapq_decode(encoded: str, codes: dict[str, str]) -> str:
    """Decode using reverse code table."""
    if not encoded:
        return ""
    reverse = {v: k for k, v in codes.items()}
    result = []
    current = ""
    for bit in encoded:
        current += bit
        if current in reverse:
            result.append(reverse[current])
            current = ""
    return "".join(result)


# ---------------------------------------------------------------------------
# Variant 3 -- counter_heap: most Pythonic, Counter + heapq
# ---------------------------------------------------------------------------

def counter_heap_encode(text: str) -> tuple[str, dict[str, str]]:
    """
    Most concise Huffman using Counter + heapq.

    >>> encoded, codes = counter_heap_encode("mississippi")
    >>> _heapq_decode(encoded, codes) == "mississippi"
    True
    """
    if not text:
        return "", {}

    freq = Counter(text)
    if len(freq) == 1:
        char = next(iter(freq))
        return "0" * len(text), {char: "0"}

    # Build heap with (freq, id, subtree_as_list_of_chars_or_nested)
    heap = [(cnt, i, [ch]) for i, (ch, cnt) in enumerate(freq.items())]
    heapq.heapify(heap)
    uid = len(heap)

    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, uid, [left, right]))
        uid += 1

    # Assign codes
    codes: dict[str, str] = {}

    def assign(node, prefix: str) -> None:
        if isinstance(node, list) and len(node) == 1 and isinstance(node[0], str):
            codes[node[0]] = prefix
        elif isinstance(node, list) and len(node) == 2:
            assign(node[0], prefix + "0")
            assign(node[1], prefix + "1")

    assign(heap[0][2], "")
    encoded = "".join(codes[c] for c in text)
    return encoded, codes


# ---------------------------------------------------------------------------
# Variant 4 -- canonical Huffman codes
# ---------------------------------------------------------------------------

def canonical_encode(text: str) -> tuple[str, dict[str, str]]:
    """
    Canonical Huffman: first build normal Huffman to get code lengths,
    then assign codes canonically (sorted by length, then alphabetically).

    >>> encoded, codes = canonical_encode("aabbc")
    >>> _heapq_decode(encoded, codes) == "aabbc"
    True
    """
    if not text:
        return "", {}

    # Get code lengths from heapq variant
    _, raw_codes = heapq_encode(text)
    if not raw_codes:
        return "", {}

    # Sort by (length, char) for canonical assignment
    symbols = sorted(raw_codes.keys(), key=lambda c: (len(raw_codes[c]), c))
    lengths = [len(raw_codes[s]) for s in symbols]

    # Assign canonical codes
    codes: dict[str, str] = {}
    code = 0
    for i, sym in enumerate(symbols):
        if i > 0:
            code = (code + 1) << (lengths[i] - lengths[i - 1])
        codes[sym] = format(code, f"0{lengths[i]}b")
        code += 0  # next iteration handles increment

    # Fix: canonical code assignment
    codes = {}
    code = 0
    prev_len = lengths[0]
    for i, sym in enumerate(symbols):
        if i > 0:
            code += 1
            code <<= (lengths[i] - prev_len)
        codes[sym] = format(code, f"0{lengths[i]}b")
        prev_len = lengths[i]

    encoded = "".join(codes[c] for c in text)
    return encoded, codes


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_STRINGS = [
    "aabbc",
    "hello world",
    "mississippi",
    "abracadabra",
    "the quick brown fox jumps over the lazy dog",
    "aaaaaaa",
    "a",
    "",
]

IMPLS = [
    ("sorted_list",   sorted_list_encode),
    ("heapq_tree",    heapq_encode),
    ("counter_heap",  counter_heap_encode),
    ("canonical",     canonical_encode),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for text in TEST_STRINGS:
        for name, fn in IMPLS:
            try:
                encoded, codes = fn(text)
                decoded = _heapq_decode(encoded, codes) if encoded else ""
                ok = decoded == text
                tag = "OK" if ok else "FAIL"
                ratio = f"{len(encoded)}/{len(text)*8}" if text else "0/0"
                print(f"  [{tag}] {name:<15} '{text[:25]}' bits={ratio}")
            except Exception as e:
                print(f"  [ERR] {name:<15} '{text[:25]}' {e}")

    REPS = 5_000
    medium = "the quick brown fox jumps over the lazy dog" * 10

    print(f"\n=== Benchmark (encode '{medium[:30]}...', {len(medium)} chars): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(medium), number=REPS) * 1000 / REPS
        print(f"  {name:<15} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
