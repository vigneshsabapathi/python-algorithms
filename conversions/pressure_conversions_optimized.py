"""
Pressure Conversions - Optimized Variants with Benchmarks
"""

import timeit

PRESSURE_CHART = {
    "pascal": 1.0, "kilopascal": 1000.0, "bar": 100_000.0,
    "atmosphere": 101_325.0, "torr": 133.322, "psi": 6894.76,
}


def pressure_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through pascals.

    >>> pressure_via_base(1, "atmosphere", "bar")
    1.01325
    """
    return round(value * PRESSURE_CHART[from_u] / PRESSURE_CHART[to_u], 5)


def pressure_direct(value: float, from_u: str, to_u: str) -> float:
    """
    Direct ratio.

    >>> pressure_direct(1, "atmosphere", "bar")
    1.01325
    """
    return round(value * (PRESSURE_CHART[from_u] / PRESSURE_CHART[to_u]), 5)


def pressure_cached(value: float, from_u: str, to_u: str, _c={}) -> float:
    """
    Cached ratio.

    >>> pressure_cached(1, "atmosphere", "bar")
    1.01325
    """
    k = (from_u, to_u)
    if k not in _c:
        _c[k] = PRESSURE_CHART[from_u] / PRESSURE_CHART[to_u]
    return round(value * _c[k], 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 atm -> bar ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", pressure_via_base), ("Direct", pressure_direct),
                         ("Cached", pressure_cached)]:
        t = timeit.timeit(lambda: func(1, "atmosphere", "bar"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
