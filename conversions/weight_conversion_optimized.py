"""
Weight Conversion - Optimized Variants with Benchmarks
"""

import timeit

WEIGHT_CHART = {
    "milligram": 0.000001, "gram": 0.001, "kilogram": 1.0, "metric_ton": 1000.0,
    "ounce": 0.0283495, "pound": 0.453592, "stone": 6.35029,
}


def weight_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through base unit (kilograms).

    >>> weight_via_base(1, "kilogram", "pound")
    2.20462
    """
    return round(value * WEIGHT_CHART[from_u] / WEIGHT_CHART[to_u], 5)


def weight_direct_ratio(value: float, from_u: str, to_u: str) -> float:
    """
    Pre-compute ratio inline.

    >>> weight_direct_ratio(1, "kilogram", "pound")
    2.20462
    """
    ratio = WEIGHT_CHART[from_u] / WEIGHT_CHART[to_u]
    return round(value * ratio, 5)


def weight_cached_ratios(value: float, from_u: str, to_u: str, _cache={}) -> float:
    """
    Cached conversion ratios for repeated calls.

    >>> weight_cached_ratios(1, "kilogram", "pound")
    2.20462
    """
    key = (from_u, to_u)
    if key not in _cache:
        _cache[key] = WEIGHT_CHART[from_u] / WEIGHT_CHART[to_u]
    return round(value * _cache[key], 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 kg -> lb ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", weight_via_base),
                         ("Direct ratio", weight_direct_ratio),
                         ("Cached ratios", weight_cached_ratios)]:
        t = timeit.timeit(lambda: func(1, "kilogram", "pound"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
