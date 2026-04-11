#!/usr/bin/env python3
"""
Resonant Frequency — LC circuit resonance.

f = 1 / (2 * pi * sqrt(L * C))
Reference: https://en.wikipedia.org/wiki/LC_circuit

Run:
    python -m doctest electronics/resonant_frequency.py -v
"""

from __future__ import annotations

from math import pi, sqrt


def resonant_frequency(inductance: float, capacitance: float) -> tuple:
    """
    Calculate resonant frequency of an LC circuit.

    >>> resonant_frequency(inductance=10, capacitance=5)
    ('Resonant frequency', 0.022507907903927652)
    >>> resonant_frequency(inductance=0, capacitance=5)
    Traceback (most recent call last):
      ...
    ValueError: Inductance cannot be 0 or negative
    >>> resonant_frequency(inductance=10, capacitance=0)
    Traceback (most recent call last):
      ...
    ValueError: Capacitance cannot be 0 or negative
    """
    if inductance <= 0:
        raise ValueError("Inductance cannot be 0 or negative")
    elif capacitance <= 0:
        raise ValueError("Capacitance cannot be 0 or negative")
    else:
        return (
            "Resonant frequency",
            float(1 / (2 * pi * (sqrt(inductance * capacitance)))),
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
