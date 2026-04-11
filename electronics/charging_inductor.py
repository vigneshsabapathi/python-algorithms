#!/usr/bin/env python3
"""
Charging Inductor — RL circuit current over time.

I(t) = (V/R) * (1 - e^(-tR/L))
Reference: https://en.wikipedia.org/wiki/RL_circuit

Run:
    python -m doctest electronics/charging_inductor.py -v
"""

from math import exp


def charging_inductor(
    source_voltage: float,
    resistance: float,
    inductance: float,
    time: float,
) -> float:
    """
    Find inductor current at any nth second after initiating its charging.

    >>> charging_inductor(source_voltage=5.8, resistance=1.5, inductance=2.3, time=2)
    2.817
    >>> charging_inductor(source_voltage=8, resistance=5, inductance=3, time=2)
    1.543
    >>> charging_inductor(source_voltage=8, resistance=5*pow(10,2), inductance=3, time=2)
    0.016
    >>> charging_inductor(source_voltage=-8, resistance=100, inductance=15, time=12)
    Traceback (most recent call last):
        ...
    ValueError: Source voltage must be positive.
    >>> charging_inductor(source_voltage=80, resistance=-15, inductance=100, time=5)
    Traceback (most recent call last):
        ...
    ValueError: Resistance must be positive.
    >>> charging_inductor(source_voltage=12, resistance=200, inductance=-20, time=5)
    Traceback (most recent call last):
        ...
    ValueError: Inductance must be positive.
    >>> charging_inductor(source_voltage=0, resistance=200, inductance=20, time=5)
    Traceback (most recent call last):
        ...
    ValueError: Source voltage must be positive.
    >>> charging_inductor(source_voltage=10, resistance=0, inductance=20, time=5)
    Traceback (most recent call last):
        ...
    ValueError: Resistance must be positive.
    >>> charging_inductor(source_voltage=15, resistance=25, inductance=0, time=5)
    Traceback (most recent call last):
        ...
    ValueError: Inductance must be positive.
    """
    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if inductance <= 0:
        raise ValueError("Inductance must be positive.")
    return round(
        source_voltage / resistance * (1 - exp((-time * resistance) / inductance)), 3
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
