#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fractional Knapsack 2 (OOP).

The reference uses an Item dataclass sorted by value/weight ratio.

Variants covered:
1. dataclass_sort    -- Item dataclass with sorted() (reference)
2. namedtuple_style  -- using collections.namedtuple
3. tuple_only        -- plain tuples, no objects
4. dict_style        -- list of dicts for JSON-friendly input

Key interview insight:
    OOP vs functional tradeoff: dataclass is cleaner for interview discussion,
    tuple is faster. Both give O(n log n) from the sort.

Run:
    python greedy_methods/fractional_knapsack_2_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.fractional_knapsack_2 import Item, fractional_knapsack as reference


# ---------------------------------------------------------------------------
# Variant 1 — dataclass sort (reference)
# ---------------------------------------------------------------------------

def dataclass_sort(items: list[Item], capacity: int) -> float:
    """
    Sort Item dataclasses by ratio descending, fill greedily.

    >>> dataclass_sort([Item("A",60,10), Item("B",100,20), Item("C",120,30)], 50)
    240.0
    >>> dataclass_sort([], 50)
    0.0
    """
    sorted_items = sorted(items, key=lambda it: it.ratio, reverse=True)
    total, remaining = 0.0, capacity
    for item in sorted_items:
        if remaining <= 0:
            break
        take = min(item.weight, remaining)
        total += item.value * (take / item.weight)
        remaining -= take
    return total


# ---------------------------------------------------------------------------
# Variant 2 — namedtuple style
# ---------------------------------------------------------------------------

KnapsackItem = namedtuple("KnapsackItem", ["name", "value", "weight"])


def namedtuple_style(items: list[tuple], capacity: int) -> float:
    """
    Use namedtuples — lighter than dataclass, still readable.

    >>> items = [KnapsackItem("A",60,10), KnapsackItem("B",100,20), KnapsackItem("C",120,30)]
    >>> namedtuple_style(items, 50)
    240.0
    >>> namedtuple_style([], 50)
    0.0
    """
    sorted_items = sorted(items, key=lambda it: it.value / it.weight, reverse=True)
    total, remaining = 0.0, capacity
    for item in sorted_items:
        if remaining <= 0:
            break
        take = min(item.weight, remaining)
        total += item.value * (take / item.weight)
        remaining -= take
    return total


# ---------------------------------------------------------------------------
# Variant 3 — tuple only: (value, weight) pairs, no names
# ---------------------------------------------------------------------------

def tuple_only(items: list[tuple[int, int]], capacity: int) -> float:
    """
    Plain tuples (value, weight) — minimal overhead, maximum speed.

    >>> tuple_only([(60,10), (100,20), (120,30)], 50)
    240.0
    >>> tuple_only([], 50)
    0.0
    """
    sorted_items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    total, remaining = 0.0, capacity
    for v, w in sorted_items:
        if remaining <= 0:
            break
        take = min(w, remaining)
        total += v * (take / w)
        remaining -= take
    return total


# ---------------------------------------------------------------------------
# Variant 4 — dict style: JSON-friendly input
# ---------------------------------------------------------------------------

def dict_style(items: list[dict], capacity: int) -> float:
    """
    List of dicts with 'value' and 'weight' keys — API-friendly format.

    >>> dict_style([{"value":60,"weight":10}, {"value":100,"weight":20}, {"value":120,"weight":30}], 50)
    240.0
    >>> dict_style([], 50)
    0.0
    """
    sorted_items = sorted(
        items, key=lambda d: d["value"] / d["weight"], reverse=True
    )
    total, remaining = 0.0, capacity
    for d in sorted_items:
        if remaining <= 0:
            break
        take = min(d["weight"], remaining)
        total += d["value"] * (take / d["weight"])
        remaining -= take
    return total


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    items_dc = [Item("A", 60, 10), Item("B", 100, 20), Item("C", 120, 30)]
    items_nt = [KnapsackItem("A", 60, 10), KnapsackItem("B", 100, 20), KnapsackItem("C", 120, 30)]
    items_tp = [(60, 10), (100, 20), (120, 30)]
    items_dt = [{"value": 60, "weight": 10}, {"value": 100, "weight": 20}, {"value": 120, "weight": 30}]

    print("\n=== Correctness (capacity=50, expected=240.0) ===")
    for name, fn, data in [
        ("reference", reference, items_dc),
        ("dataclass_sort", dataclass_sort, items_dc),
        ("namedtuple_style", namedtuple_style, items_nt),
        ("tuple_only", tuple_only, items_tp),
        ("dict_style", dict_style, items_dt),
    ]:
        result = fn(data, 50)
        tag = "OK" if result == 240.0 else "FAIL"
        print(f"  [{tag}] {name:<20} = {result}")

    import random
    random.seed(42)
    big_dc = [Item(f"I{i}", random.randint(1, 100), random.randint(1, 50)) for i in range(1000)]
    big_tp = [(it.value, it.weight) for it in big_dc]
    big_dt = [{"value": it.value, "weight": it.weight} for it in big_dc]
    big_nt = [KnapsackItem(it.name, it.value, it.weight) for it in big_dc]

    REPS = 10_000
    print(f"\n=== Benchmark (1000 items, cap=500): {REPS} runs ===")
    for name, fn, data in [
        ("reference", reference, big_dc),
        ("dataclass_sort", dataclass_sort, big_dc),
        ("namedtuple_style", namedtuple_style, big_nt),
        ("tuple_only", tuple_only, big_tp),
        ("dict_style", dict_style, big_dt),
    ]:
        t = timeit.timeit(lambda fn=fn, d=data: fn(d, 500), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
