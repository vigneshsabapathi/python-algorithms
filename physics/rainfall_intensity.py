"""
Rainfall Intensity (IDF - Intensity-Duration-Frequency).

A simplified rainfall intensity formula:
    i = a / (t + b)

where:
    i = rainfall intensity (mm/hr)
    t = duration (minutes)
    a, b = empirical constants for the region

Also: Sherman equation: i = K * T^a / (t + b)^c
where T = return period (years), K, a, b, c are regional constants.

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/rainfall_intensity.py
"""


def rainfall_intensity(
    coefficient_a: float, duration: float, coefficient_b: float = 10.0
) -> float:
    """
    Calculate rainfall intensity using the simplified IDF formula.

    >>> round(rainfall_intensity(1000, 30), 4)
    25.0
    >>> round(rainfall_intensity(1000, 60), 4)
    14.2857
    >>> round(rainfall_intensity(500, 15, 5), 4)
    25.0
    >>> rainfall_intensity(1000, -1)
    Traceback (most recent call last):
        ...
    ValueError: duration must be non-negative
    >>> rainfall_intensity(-1, 30)
    Traceback (most recent call last):
        ...
    ValueError: coefficient_a must be positive
    """
    if coefficient_a <= 0:
        raise ValueError("coefficient_a must be positive")
    if duration < 0:
        raise ValueError("duration must be non-negative")
    if coefficient_b < 0:
        raise ValueError("coefficient_b must be non-negative")
    if duration + coefficient_b == 0:
        raise ValueError("duration + coefficient_b must not be zero")

    return coefficient_a / (duration + coefficient_b)


def sherman_intensity(
    k: float,
    return_period: float,
    duration: float,
    a: float = 0.2,
    b: float = 10.0,
    c: float = 0.8,
) -> float:
    """
    Calculate rainfall intensity using the Sherman equation.

    >>> round(sherman_intensity(1000, 10, 30), 4)
    82.8614
    >>> round(sherman_intensity(1000, 25, 60), 4)
    63.6077
    """
    if k <= 0:
        raise ValueError("k must be positive")
    if return_period <= 0:
        raise ValueError("return_period must be positive")
    if duration < 0:
        raise ValueError("duration must be non-negative")

    return k * return_period**a / (duration + b) ** c


if __name__ == "__main__":
    import doctest

    doctest.testmod()
