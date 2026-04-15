"""
Interquartile Range (IQR) = Q3 - Q1. Measures statistical dispersion.

>>> iqr([1, 2, 3, 4, 5, 6, 7, 8, 9])
4.0
>>> iqr([1, 2, 3, 4])
1.5
>>> iqr([4, 4, 4, 4])
0.0
"""


def _quantile(sorted_data: list[float], q: float) -> float:
    """Linear interpolation quantile (like numpy default)."""
    n = len(sorted_data)
    pos = (n - 1) * q
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return sorted_data[lo] * (1 - frac) + sorted_data[hi] * frac


def iqr(data: list[float]) -> float:
    """Compute Q3 - Q1.

    >>> iqr([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    45.0
    """
    if not data:
        raise ValueError("empty list")
    s = sorted(data)
    return _quantile(s, 0.75) - _quantile(s, 0.25)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(iqr([1, 2, 3, 4, 5, 6, 7, 8, 9]))
