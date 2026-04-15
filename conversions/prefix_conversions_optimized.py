"""
Prefix Conversions - Optimized Variants with Benchmarks
"""

import timeit

SI_PREFIXES = {
    "nano": 1e-9, "micro": 1e-6, "milli": 1e-3, "centi": 1e-2,
    "base": 1.0, "kilo": 1e3, "mega": 1e6, "giga": 1e9, "tera": 1e12,
}


def prefix_via_base(value: float, from_p: str, to_p: str) -> float:
    """
    Convert through base unit.

    >>> prefix_via_base(1, "kilo", "base")
    1000.0
    """
    return round(value * SI_PREFIXES[from_p] / SI_PREFIXES[to_p], 10)


def prefix_log_ratio(value: float, from_p: str, to_p: str) -> float:
    """
    Direct ratio multiplication.

    >>> prefix_log_ratio(1, "kilo", "base")
    1000.0
    """
    return round(value * (SI_PREFIXES[from_p] / SI_PREFIXES[to_p]), 10)


def prefix_cached(value: float, from_p: str, to_p: str, _c={}) -> float:
    """
    Cached ratio.

    >>> prefix_cached(1, "kilo", "base")
    1000.0
    """
    k = (from_p, to_p)
    if k not in _c:
        _c[k] = SI_PREFIXES[from_p] / SI_PREFIXES[to_p]
    return round(value * _c[k], 10)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 kilo -> base ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", prefix_via_base), ("Log ratio", prefix_log_ratio),
                         ("Cached", prefix_cached)]:
        t = timeit.timeit(lambda: func(1, "kilo", "base"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
