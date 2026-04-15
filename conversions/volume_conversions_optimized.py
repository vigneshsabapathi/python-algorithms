"""
Volume Conversions - Optimized Variants with Benchmarks
"""

import timeit

VOLUME_CHART = {
    "milliliter": 0.001, "liter": 1.0, "gallon": 3.78541,
    "quart": 0.946353, "pint": 0.473176, "cup": 0.236588,
}


def volume_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through liters.

    >>> volume_via_base(1, "gallon", "liter")
    3.78541
    """
    return round(value * VOLUME_CHART[from_u] / VOLUME_CHART[to_u], 5)


def volume_direct(value: float, from_u: str, to_u: str) -> float:
    """
    Direct ratio.

    >>> volume_direct(1, "gallon", "liter")
    3.78541
    """
    return round(value * (VOLUME_CHART[from_u] / VOLUME_CHART[to_u]), 5)


def volume_cached(value: float, from_u: str, to_u: str, _c={}) -> float:
    """
    Cached ratio.

    >>> volume_cached(1, "gallon", "liter")
    3.78541
    """
    k = (from_u, to_u)
    if k not in _c:
        _c[k] = VOLUME_CHART[from_u] / VOLUME_CHART[to_u]
    return round(value * _c[k], 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 gallon -> liter ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", volume_via_base), ("Direct", volume_direct),
                         ("Cached", volume_cached)]:
        t = timeit.timeit(lambda: func(1, "gallon", "liter"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
