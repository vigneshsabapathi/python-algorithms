"""
Length Conversion - Optimized Variants with Benchmarks
"""

import timeit

LENGTH_CHART = {
    "millimeter": 0.001, "centimeter": 0.01, "meter": 1.0, "kilometer": 1000.0,
    "inch": 0.0254, "foot": 0.3048, "yard": 0.9144, "mile": 1609.344,
}


def length_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through base unit (meters).

    >>> length_via_base(1, "mile", "kilometer")
    1.609344
    """
    return round(value * LENGTH_CHART[from_u] / LENGTH_CHART[to_u], 10)


def length_direct_table(value: float, from_u: str, to_u: str) -> float:
    """
    Pre-computed direct conversion ratios (cached).

    >>> length_direct_table(1, "mile", "kilometer")
    1.609344
    """
    _ratios = {}
    key = (from_u, to_u)
    if key not in _ratios:
        _ratios[key] = LENGTH_CHART[from_u] / LENGTH_CHART[to_u]
    return round(value * _ratios[key], 10)


def length_multiplication_chain(value: float, from_u: str, to_u: str) -> float:
    """
    Multiply by from-factor, divide by to-factor (same math, different style).

    >>> length_multiplication_chain(1, "mile", "kilometer")
    1.609344
    """
    return round(value * (LENGTH_CHART[from_u] / LENGTH_CHART[to_u]), 10)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 mile -> km ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", length_via_base),
                         ("Direct table", length_direct_table),
                         ("Mult chain", length_multiplication_chain)]:
        t = timeit.timeit(lambda: func(1, "mile", "kilometer"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
