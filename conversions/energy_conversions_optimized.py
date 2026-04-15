"""
Energy Conversions - Optimized Variants with Benchmarks
"""

import timeit

ENERGY_CHART = {
    "joule": 1.0, "kilojoule": 1000.0, "calorie": 4.184,
    "kilocalorie": 4184.0, "kilowatt_hour": 3_600_000.0,
}


def energy_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through joules.

    >>> energy_via_base(1, "kilocalorie", "kilojoule")
    4.184
    """
    return round(value * ENERGY_CHART[from_u] / ENERGY_CHART[to_u], 5)


def energy_direct(value: float, from_u: str, to_u: str) -> float:
    """
    Direct ratio.

    >>> energy_direct(1, "kilocalorie", "kilojoule")
    4.184
    """
    return round(value * (ENERGY_CHART[from_u] / ENERGY_CHART[to_u]), 5)


def energy_cached(value: float, from_u: str, to_u: str, _c={}) -> float:
    """
    Cached ratio.

    >>> energy_cached(1, "kilocalorie", "kilojoule")
    4.184
    """
    k = (from_u, to_u)
    if k not in _c:
        _c[k] = ENERGY_CHART[from_u] / ENERGY_CHART[to_u]
    return round(value * _c[k], 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 kcal -> kJ ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", energy_via_base), ("Direct", energy_direct),
                         ("Cached", energy_cached)]:
        t = timeit.timeit(lambda: func(1, "kilocalorie", "kilojoule"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
