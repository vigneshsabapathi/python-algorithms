#!/usr/bin/env python3
"""
Charging Capacitor — RC circuit voltage over time.

V(t) = V_source * (1 - e^(-t / RC))
Reference: https://en.wikipedia.org/wiki/RC_time_constant

Run:
    python -m doctest electronics/charging_capacitor.py -v
"""

from math import exp


def charging_capacitor(
    source_voltage: float,
    resistance: float,
    capacitance: float,
    time_sec: float,
) -> float:
    """
    Find capacitor voltage at any nth second after initiating its charging.

    >>> charging_capacitor(source_voltage=.2, resistance=.9, capacitance=8.4, time_sec=.5)
    0.013
    >>> charging_capacitor(source_voltage=2.2, resistance=3.5, capacitance=2.4, time_sec=9)
    1.446
    >>> charging_capacitor(source_voltage=15, resistance=200, capacitance=20, time_sec=2)
    0.007
    >>> charging_capacitor(20, 2000, 30*pow(10,-5), 4)
    19.975
    >>> charging_capacitor(source_voltage=0, resistance=10.0, capacitance=.30, time_sec=3)
    Traceback (most recent call last):
        ...
    ValueError: Source voltage must be positive.
    >>> charging_capacitor(source_voltage=20, resistance=-2000, capacitance=30, time_sec=4)
    Traceback (most recent call last):
        ...
    ValueError: Resistance must be positive.
    >>> charging_capacitor(source_voltage=30, resistance=1500, capacitance=0, time_sec=4)
    Traceback (most recent call last):
        ...
    ValueError: Capacitance must be positive.
    """
    if source_voltage <= 0:
        raise ValueError("Source voltage must be positive.")
    if resistance <= 0:
        raise ValueError("Resistance must be positive.")
    if capacitance <= 0:
        raise ValueError("Capacitance must be positive.")
    return round(source_voltage * (1 - exp(-time_sec / (resistance * capacitance))), 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
