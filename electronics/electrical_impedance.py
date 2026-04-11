#!/usr/bin/env python3
"""
Electrical Impedance — Z = sqrt(R^2 + X^2).

Reference: https://en.wikipedia.org/wiki/Electrical_impedance

Run:
    python -m doctest electronics/electrical_impedance.py -v
"""

from __future__ import annotations

from math import pow, sqrt  # noqa: A004


def electrical_impedance(
    resistance: float, reactance: float, impedance: float
) -> dict[str, float]:
    """
    Apply Electrical Impedance formula on any two given values (set unknown to 0).

    >>> electrical_impedance(3, 4, 0)
    {'impedance': 5.0}
    >>> electrical_impedance(0, 4, 5)
    {'resistance': 3.0}
    >>> electrical_impedance(3, 0, 5)
    {'reactance': 4.0}
    >>> electrical_impedance(3, 4, 5)
    Traceback (most recent call last):
      ...
    ValueError: One and only one argument must be 0
    """
    if (resistance, reactance, impedance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if resistance == 0:
        return {"resistance": sqrt(pow(impedance, 2) - pow(reactance, 2))}
    elif reactance == 0:
        return {"reactance": sqrt(pow(impedance, 2) - pow(resistance, 2))}
    elif impedance == 0:
        return {"impedance": sqrt(pow(resistance, 2) + pow(reactance, 2))}
    else:
        raise ValueError("Exactly one argument must be 0")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
