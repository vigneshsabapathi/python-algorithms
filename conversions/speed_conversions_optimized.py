"""
Speed Conversions - Optimized Variants with Benchmarks
"""

import timeit

SPEED_CHART = {
    "meters_per_second": 1.0, "kilometers_per_hour": 0.277778,
    "miles_per_hour": 0.44704, "knot": 0.514444,
}


def speed_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through m/s.

    >>> speed_via_base(1, "meters_per_second", "kilometers_per_hour")
    3.6
    """
    return round(value * SPEED_CHART[from_u] / SPEED_CHART[to_u], 5)


def speed_direct(value: float, from_u: str, to_u: str) -> float:
    """
    Direct ratio computation.

    >>> speed_direct(1, "meters_per_second", "kilometers_per_hour")
    3.6
    """
    return round(value * (SPEED_CHART[from_u] / SPEED_CHART[to_u]), 5)


def speed_cached(value: float, from_u: str, to_u: str, _c={}) -> float:
    """
    Cached ratio for repeated conversions.

    >>> speed_cached(1, "meters_per_second", "kilometers_per_hour")
    3.6
    """
    k = (from_u, to_u)
    if k not in _c:
        _c[k] = SPEED_CHART[from_u] / SPEED_CHART[to_u]
    return round(value * _c[k], 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 m/s -> km/h ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", speed_via_base), ("Direct", speed_direct),
                         ("Cached", speed_cached)]:
        t = timeit.timeit(lambda: func(1, "meters_per_second", "kilometers_per_hour"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
