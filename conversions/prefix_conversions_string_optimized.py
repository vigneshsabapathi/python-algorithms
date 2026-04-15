"""
Prefix Conversions String - Optimized Variants with Benchmarks
"""

import timeit

SI_PREFIX_SYMBOLS = {
    "n": 1e-9, "u": 1e-6, "m": 1e-3, "c": 1e-2,
    "": 1.0, "k": 1e3, "M": 1e6, "G": 1e9, "T": 1e12,
}


def add_prefix_loop(value: float, unit: str = "m") -> str:
    """
    Loop through prefixes to find best.

    >>> add_prefix_loop(1000, "g")
    '1.0 kg'
    """
    if value == 0:
        return f"0.0 {unit}"
    sorted_p = sorted(SI_PREFIX_SYMBOLS.items(), key=lambda x: x[1])
    best = ""
    for sym, fac in sorted_p:
        if fac <= abs(value):
            best = sym
    return f"{value / SI_PREFIX_SYMBOLS[best]:.1f} {best}{unit}"


def add_prefix_binary_search(value: float, unit: str = "m") -> str:
    """
    Binary search for best prefix.

    >>> add_prefix_binary_search(1000, "g")
    '1.0 kg'
    """
    if value == 0:
        return f"0.0 {unit}"
    import bisect
    sorted_items = sorted(SI_PREFIX_SYMBOLS.items(), key=lambda x: x[1])
    factors = [f for _, f in sorted_items]
    idx = bisect.bisect_right(factors, abs(value)) - 1
    idx = max(0, idx)
    sym = sorted_items[idx][0]
    return f"{value / SI_PREFIX_SYMBOLS[sym]:.1f} {sym}{unit}"


def add_prefix_precomputed(value: float, unit: str = "m") -> str:
    """
    Pre-sorted prefix list (avoids re-sorting).

    >>> add_prefix_precomputed(1000, "g")
    '1.0 kg'
    """
    _sorted = [("n", 1e-9), ("u", 1e-6), ("m", 1e-3), ("c", 1e-2),
               ("", 1.0), ("k", 1e3), ("M", 1e6), ("G", 1e9), ("T", 1e12)]
    if value == 0:
        return f"0.0 {unit}"
    best_sym, best_fac = "", 1.0
    for sym, fac in _sorted:
        if fac <= abs(value):
            best_sym, best_fac = sym, fac
    return f"{value / best_fac:.1f} {best_sym}{unit}"


def benchmark():
    number = 200_000
    test_val = 1500.0
    print(f"Benchmark: add_prefix({test_val}) ({number:,} iterations)\n")
    results = []
    for label, func in [("Loop", add_prefix_loop),
                         ("Binary search", add_prefix_binary_search),
                         ("Precomputed", add_prefix_precomputed)]:
        t = timeit.timeit(lambda: func(test_val, "m"), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
