"""
Temperature Conversions - Optimized Variants with Benchmarks
"""

import timeit


def celsius_to_fahrenheit_formula(c: float) -> float:
    """
    Standard formula: F = C * 9/5 + 32.

    >>> celsius_to_fahrenheit_formula(100)
    212.0
    """
    return round(c * 9 / 5 + 32, 2)


def celsius_to_fahrenheit_multiply(c: float) -> float:
    """
    Optimized: F = C * 1.8 + 32 (avoids division).

    >>> celsius_to_fahrenheit_multiply(100)
    212.0
    """
    return round(c * 1.8 + 32, 2)


def celsius_to_fahrenheit_lookup(c: float) -> float:
    """
    Pre-computed lookup for integer Celsius values (-50 to 150).

    >>> celsius_to_fahrenheit_lookup(100)
    212.0
    """
    _cache = {}
    int_c = int(c)
    if int_c == c and -50 <= int_c <= 150:
        if int_c not in _cache:
            _cache[int_c] = round(int_c * 1.8 + 32, 2)
        return _cache[int_c]
    return round(c * 1.8 + 32, 2)


def benchmark():
    number = 200_000
    test_val = 37.5
    print(f"Benchmark: C->F for {test_val} ({number:,} iterations)\n")
    results = []
    for label, func in [("Formula (9/5)", celsius_to_fahrenheit_formula),
                         ("Multiply (1.8)", celsius_to_fahrenheit_multiply),
                         ("Lookup cache", celsius_to_fahrenheit_lookup)]:
        t = timeit.timeit(lambda: func(test_val), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
