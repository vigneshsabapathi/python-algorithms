"""
Astronomical Length Scale Conversion - Optimized Variants with Benchmarks
"""

import timeit

ASTRO_UNITS = {
    "meter": 1.0, "kilometer": 1e3, "astronomical_unit": 1.495978707e11,
    "light_year": 9.4607304725808e15, "parsec": 3.0856775814913673e16,
}


def astro_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through meters.

    >>> astro_via_base(1, "parsec", "light_year")
    3.26156
    """
    return round(value * ASTRO_UNITS[from_u] / ASTRO_UNITS[to_u], 5)


def astro_direct(value: float, from_u: str, to_u: str) -> float:
    """
    Direct ratio.

    >>> astro_direct(1, "parsec", "light_year")
    3.26156
    """
    return round(value * (ASTRO_UNITS[from_u] / ASTRO_UNITS[to_u]), 5)


def astro_cached(value: float, from_u: str, to_u: str, _c={}) -> float:
    """
    Cached ratio.

    >>> astro_cached(1, "parsec", "light_year")
    3.26156
    """
    k = (from_u, to_u)
    if k not in _c:
        _c[k] = ASTRO_UNITS[from_u] / ASTRO_UNITS[to_u]
    return round(value * _c[k], 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 parsec -> ly ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", astro_via_base), ("Direct", astro_direct),
                         ("Cached", astro_cached)]:
        t = timeit.timeit(lambda: func(1, "parsec", "light_year"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
