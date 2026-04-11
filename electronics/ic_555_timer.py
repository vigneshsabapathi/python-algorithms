#!/usr/bin/env python3
"""
IC 555 Timer — astable mode frequency and duty cycle.

Freq = 1.44 / [(R1 + 2*R2) * C1]
Duty Cycle = (R1 + R2) / (R1 + 2*R2) * 100
Reference: https://en.wikipedia.org/wiki/555_timer_IC#Astable

Run:
    python -m doctest electronics/ic_555_timer.py -v
"""

from __future__ import annotations


def astable_frequency(
    resistance_1: float, resistance_2: float, capacitance: float
) -> float:
    """
    Calculate astable 555 timer frequency in Hz.
    Capacitance in microfarads, resistances in ohms.

    >>> astable_frequency(resistance_1=45, resistance_2=45, capacitance=7)
    1523.8095238095239
    >>> astable_frequency(resistance_1=356, resistance_2=234, capacitance=976)
    1.7905459175553078
    >>> astable_frequency(resistance_1=2, resistance_2=-1, capacitance=2)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    >>> astable_frequency(resistance_1=45, resistance_2=45, capacitance=0)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    """
    if resistance_1 <= 0 or resistance_2 <= 0 or capacitance <= 0:
        raise ValueError("All values must be positive")
    return (1.44 / ((resistance_1 + 2 * resistance_2) * capacitance)) * 10**6


def astable_duty_cycle(resistance_1: float, resistance_2: float) -> float:
    """
    Calculate astable 555 timer duty cycle in percent.

    >>> astable_duty_cycle(resistance_1=45, resistance_2=45)
    66.66666666666666
    >>> astable_duty_cycle(resistance_1=356, resistance_2=234)
    71.60194174757282
    >>> astable_duty_cycle(resistance_1=2, resistance_2=-1)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    >>> astable_duty_cycle(resistance_1=0, resistance_2=0)
    Traceback (most recent call last):
        ...
    ValueError: All values must be positive
    """
    if resistance_1 <= 0 or resistance_2 <= 0:
        raise ValueError("All values must be positive")
    return (resistance_1 + resistance_2) / (resistance_1 + 2 * resistance_2) * 100


if __name__ == "__main__":
    import doctest

    doctest.testmod()
