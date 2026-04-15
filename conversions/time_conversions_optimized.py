"""
Time Conversions - Optimized Variants with Benchmarks
"""

import timeit

TIME_CHART = {
    "millisecond": 0.001, "second": 1.0, "minute": 60.0,
    "hour": 3600.0, "day": 86400.0, "week": 604800.0,
}


def time_via_base(value: float, from_u: str, to_u: str) -> float:
    """
    Convert through seconds.

    >>> time_via_base(1, "hour", "minute")
    60.0
    """
    return round(value * TIME_CHART[from_u] / TIME_CHART[to_u], 5)


def time_direct(value: float, from_u: str, to_u: str) -> float:
    """
    Direct ratio.

    >>> time_direct(1, "hour", "minute")
    60.0
    """
    return round(value * (TIME_CHART[from_u] / TIME_CHART[to_u]), 5)


def time_cached(value: float, from_u: str, to_u: str, _c={}) -> float:
    """
    Cached ratio.

    >>> time_cached(1, "hour", "minute")
    60.0
    """
    k = (from_u, to_u)
    if k not in _c:
        _c[k] = TIME_CHART[from_u] / TIME_CHART[to_u]
    return round(value * _c[k], 5)


def benchmark():
    number = 200_000
    print(f"Benchmark: 1 hour -> min ({number:,} iterations)\n")
    results = []
    for label, func in [("Via base", time_via_base), ("Direct", time_direct),
                         ("Cached", time_cached)]:
        t = timeit.timeit(lambda: func(1, "hour", "minute"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
