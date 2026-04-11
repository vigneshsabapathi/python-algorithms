#!/usr/bin/env python3
"""
Optimized and alternative implementations of fuzzy set operations.

The reference uses a dataclass-based FuzzySet with triangular membership.
Here we explore multiple representation and computation strategies.

Variants covered:
1. dataclass_based   -- FuzzySet dataclass with method calls (reference)
2. dict_based        -- Lightweight dict representation, plain functions
3. numpy_vectorized  -- NumPy-accelerated batch membership over arrays
4. functional_lambda -- Sets as closures (membership-function-first design)
5. interval_arith    -- Pure interval arithmetic for alpha-cuts

Key interview insight:
    Fuzzy logic interviews test understanding of membership functions,
    t-norms (intersection), t-conorms (union), and defuzzification.
    The dataclass approach is cleanest for OOP questions; the functional
    approach shows FP fluency; NumPy shows you can scale to real systems.

Run:
    python fuzzy_logic/fuzzy_operations_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fuzzy_logic.fuzzy_operations import FuzzySet as reference_cls


# ---------------------------------------------------------------------------
# Variant 1 — Dataclass-based (reference wrapper)
# ---------------------------------------------------------------------------

def membership_dataclass(left: float, peak: float, right: float, x: float) -> float:
    """
    Membership via the reference FuzzySet class.

    >>> membership_dataclass(0, 0.5, 1, 0.25)
    0.5
    >>> membership_dataclass(0, 0.5, 1, 0.75)
    0.5
    >>> membership_dataclass(0, 0.5, 1, 0.0)
    0.0
    """
    fs = reference_cls("tmp", left, peak, right)
    return fs.membership(x)


# ---------------------------------------------------------------------------
# Variant 2 — Dict-based, plain functions (no class overhead)
# ---------------------------------------------------------------------------

def make_fuzzy_dict(name: str, left: float, peak: float, right: float) -> dict:
    """
    Create a fuzzy set as a plain dictionary.

    >>> make_fuzzy_dict("A", 0, 0.5, 1)
    {'name': 'A', 'left': 0, 'peak': 0.5, 'right': 1}
    """
    return {"name": name, "left": left, "peak": peak, "right": right}


def membership_dict(fs: dict, x: float) -> float:
    """
    Triangular membership using a dict-based fuzzy set.

    >>> fs = make_fuzzy_dict("A", 0, 0.5, 1)
    >>> membership_dict(fs, 0.25)
    0.5
    >>> membership_dict(fs, 0.75)
    0.5
    >>> membership_dict(fs, 0.0)
    0.0
    """
    left, peak, right = fs["left"], fs["peak"], fs["right"]
    if x <= left or x >= right:
        return 0.0
    if x <= peak:
        return (x - left) / (peak - left) if peak != left else 1.0
    return (right - x) / (right - peak) if right != peak else 1.0


def complement_dict(fs: dict) -> dict:
    """
    Complement of a dict-based fuzzy set.

    >>> complement_dict(make_fuzzy_dict("A", 0.1, 0.2, 0.3))
    {'name': 'NOT A', 'left': 0.7, 'peak': 0.8, 'right': 0.9}
    """
    return {
        "name": f"NOT {fs['name']}",
        "left": round(1 - fs["right"], 10),
        "peak": round(1 - fs["peak"], 10),
        "right": round(1 - fs["left"], 10),
    }


def union_dict(a: dict, b: dict) -> dict:
    """
    Union of two dict-based fuzzy sets.

    >>> union_dict(make_fuzzy_dict("A", 0, 0.5, 1), make_fuzzy_dict("B", 0.2, 0.7, 1))
    {'name': 'A OR B', 'left': 0, 'peak': 0.7, 'right': 1}
    """
    return {
        "name": f"{a['name']} OR {b['name']}",
        "left": min(a["left"], b["left"]),
        "peak": max(a["peak"], b["peak"]),
        "right": max(a["right"], b["right"]),
    }


def intersection_dict(a: dict, b: dict) -> dict:
    """
    Intersection of two dict-based fuzzy sets.

    >>> intersection_dict(make_fuzzy_dict("A", 0, 0.5, 1), make_fuzzy_dict("B", 0.2, 0.7, 1))
    {'name': 'A AND B', 'left': 0.2, 'peak': 0.5, 'right': 1}
    """
    left = max(a["left"], b["left"])
    right = max(a["right"], b["right"])
    peak = min(a["peak"], b["peak"])
    peak = max(peak, left)
    peak = min(peak, right)
    return {
        "name": f"{a['name']} AND {b['name']}",
        "left": left,
        "peak": peak,
        "right": right,
    }


# ---------------------------------------------------------------------------
# Variant 3 — NumPy vectorized batch membership
# ---------------------------------------------------------------------------

def membership_numpy(left: float, peak: float, right: float, xs: list) -> list:
    """
    Vectorized membership computation over an array of x values.

    >>> result = membership_numpy(0, 0.5, 1, [0.0, 0.25, 0.5, 0.75, 1.0])
    >>> [round(v, 4) for v in result]
    [0.0, 0.5, 1.0, 0.5, 0.0]
    """
    try:
        import numpy as np
    except ImportError:
        return [membership_dict({"left": left, "peak": peak, "right": right}, x) for x in xs]

    arr = np.asarray(xs, dtype=float)
    result = np.zeros_like(arr)

    # Rising edge: left < x <= peak
    rising = (arr > left) & (arr <= peak)
    if peak != left:
        result[rising] = (arr[rising] - left) / (peak - left)
    else:
        result[rising] = 1.0

    # Falling edge: peak < x < right
    falling = (arr > peak) & (arr < right)
    if right != peak:
        result[falling] = (right - arr[falling]) / (right - peak)
    else:
        result[falling] = 1.0

    return result.tolist()


# ---------------------------------------------------------------------------
# Variant 4 — Functional / closure-based fuzzy sets
# ---------------------------------------------------------------------------

def make_triangular(name: str, left: float, peak: float, right: float):
    """
    Return a membership function (closure) for a triangular fuzzy set.

    >>> mu = make_triangular("A", 0, 0.5, 1)
    >>> mu(0.25)
    0.5
    >>> mu(0.75)
    0.5
    >>> mu(0.0)
    0.0
    """
    def membership(x: float) -> float:
        if x <= left or x >= right:
            return 0.0
        if x <= peak:
            return (x - left) / (peak - left) if peak != left else 1.0
        return (right - x) / (right - peak) if right != peak else 1.0
    membership.__name__ = name
    return membership


def fuzzy_union_func(mu_a, mu_b):
    """
    Return a new membership function: max(mu_a(x), mu_b(x)).

    >>> a = make_triangular("A", 0, 0.3, 0.6)
    >>> b = make_triangular("B", 0.4, 0.7, 1.0)
    >>> u = fuzzy_union_func(a, b)
    >>> round(u(0.5), 4)
    0.3333
    """
    def union(x: float) -> float:
        return max(mu_a(x), mu_b(x))
    return union


def fuzzy_intersection_func(mu_a, mu_b):
    """
    Return a new membership function: min(mu_a(x), mu_b(x)).

    >>> a = make_triangular("A", 0, 0.3, 0.6)
    >>> b = make_triangular("B", 0.4, 0.7, 1.0)
    >>> i = fuzzy_intersection_func(a, b)
    >>> round(i(0.5), 4)
    0.3333
    """
    def intersection(x: float) -> float:
        return min(mu_a(x), mu_b(x))
    return intersection


def fuzzy_complement_func(mu_a):
    """
    Return a new membership function: 1 - mu_a(x).

    >>> a = make_triangular("A", 0, 0.5, 1)
    >>> c = fuzzy_complement_func(a)
    >>> c(0.25)
    0.5
    >>> c(0.5)
    0.0
    """
    def complement(x: float) -> float:
        return 1.0 - mu_a(x)
    return complement


# ---------------------------------------------------------------------------
# Variant 5 — Interval arithmetic for alpha-cuts
# ---------------------------------------------------------------------------

def alpha_cut_interval(left: float, peak: float, right: float, alpha: float) -> tuple | None:
    """
    Compute the alpha-cut [x_low, x_high] using interval arithmetic.

    >>> alpha_cut_interval(0, 0.5, 1, 0.5)
    (0.25, 0.75)
    >>> alpha_cut_interval(0, 0.5, 1, 1.0)
    (0.5, 0.5)
    >>> alpha_cut_interval(0, 0.5, 1, 0.0) is None
    True
    """
    if alpha <= 0 or alpha > 1:
        return None
    x_low = left + alpha * (peak - left)
    x_high = right - alpha * (right - peak)
    return (round(x_low, 10), round(x_high, 10))


def centroid_interval(left: float, peak: float, right: float) -> float:
    """
    Analytical centroid of a triangular fuzzy set = (left + peak + right) / 3.

    This is exact for triangular functions (no numerical integration needed).

    >>> round(centroid_interval(0, 0.5, 1), 4)
    0.5
    >>> round(centroid_interval(0.2, 0.7, 1), 4)
    0.6333
    """
    return round((left + peak + right) / 3, 10)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare all variants on repeated membership + operation calls."""
    n_runs = 50_000
    x_val = 0.35

    # Setup data
    left, peak, right = 0.0, 0.5, 1.0
    left2, peak2, right2 = 0.2, 0.7, 1.0

    ref = reference_cls("A", left, peak, right)
    ref2 = reference_cls("B", left2, peak2, right2)
    d = make_fuzzy_dict("A", left, peak, right)
    d2 = make_fuzzy_dict("B", left2, peak2, right2)
    mu_a = make_triangular("A", left, peak, right)
    mu_b = make_triangular("B", left2, peak2, right2)

    print(f"Benchmark: {n_runs:,} iterations each\n")
    print(f"{'Variant':<28} {'Operation':<16} {'Time (ms)':>10} {'Ratio':>8}")
    print("-" * 65)

    results = []

    # --- Membership ---
    t1 = timeit.timeit(lambda: ref.membership(x_val), number=n_runs)
    results.append(("1. Dataclass", "membership", t1))

    t2 = timeit.timeit(lambda: membership_dict(d, x_val), number=n_runs)
    results.append(("2. Dict-based", "membership", t2))

    t3_setup = membership_numpy  # warm up
    xs_batch = [x_val]
    t3 = timeit.timeit(lambda: membership_numpy(left, peak, right, xs_batch), number=n_runs)
    results.append(("3. NumPy (1 elem)", "membership", t3))

    t4 = timeit.timeit(lambda: mu_a(x_val), number=n_runs)
    results.append(("4. Functional", "membership", t4))

    # --- Complement ---
    t5 = timeit.timeit(lambda: ref.complement(), number=n_runs)
    results.append(("1. Dataclass", "complement", t5))

    t6 = timeit.timeit(lambda: complement_dict(d), number=n_runs)
    results.append(("2. Dict-based", "complement", t6))

    t7 = timeit.timeit(lambda: fuzzy_complement_func(mu_a), number=n_runs)
    results.append(("4. Functional", "complement", t7))

    # --- Union ---
    t8 = timeit.timeit(lambda: ref.union(ref2), number=n_runs)
    results.append(("1. Dataclass", "union", t8))

    t9 = timeit.timeit(lambda: union_dict(d, d2), number=n_runs)
    results.append(("2. Dict-based", "union", t9))

    t10 = timeit.timeit(lambda: fuzzy_union_func(mu_a, mu_b), number=n_runs)
    results.append(("4. Functional", "union", t10))

    # --- Centroid ---
    t11 = timeit.timeit(lambda: ref.centroid(100), number=n_runs // 10)
    results.append(("1. Dataclass (n=100)", "centroid", t11))

    t12 = timeit.timeit(lambda: centroid_interval(left, peak, right), number=n_runs)
    results.append(("5. Analytical", "centroid", t12))

    # --- Batch membership (NumPy advantage) ---
    xs_large = [i / 100 for i in range(101)]
    t13 = timeit.timeit(
        lambda: [ref.membership(x) for x in xs_large], number=n_runs // 50
    )
    results.append(("1. Dataclass (101pts)", "batch memb", t13))

    t14 = timeit.timeit(
        lambda: membership_numpy(left, peak, right, xs_large), number=n_runs // 50
    )
    results.append(("3. NumPy (101pts)", "batch memb", t14))

    # Print grouped by operation
    base_times = {}
    for name, op, t in results:
        key = op
        if key not in base_times:
            base_times[key] = t
        ratio = t / base_times[key] if base_times[key] > 0 else 0
        print(f"{name:<28} {op:<16} {t * 1000:>9.2f}ms {ratio:>7.2f}x")

    print("\n--- Key Takeaways ---")
    print("- Dict-based and functional closures beat dataclass for raw membership")
    print("- NumPy shines on batch operations (101+ points)")
    print("- Analytical centroid is O(1) vs O(n) numerical integration")
    print("- Functional approach has near-zero overhead for complement/union creation")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
