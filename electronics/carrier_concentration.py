#!/usr/bin/env python3
"""
Carrier Concentration — mass action law for semiconductors.

ni^2 = n * p  (electron_conc * hole_conc = intrinsic_conc^2)
Reference: https://en.wikipedia.org/wiki/Charge_carrier_density

Run:
    python -m doctest electronics/carrier_concentration.py -v
"""

from __future__ import annotations


def carrier_concentration(
    electron_conc: float,
    hole_conc: float,
    intrinsic_conc: float,
) -> tuple:
    """
    Calculate any one of {electron_conc, hole_conc, intrinsic_conc}
    given the other two (set the unknown to 0).

    >>> carrier_concentration(electron_conc=25, hole_conc=100, intrinsic_conc=0)
    ('intrinsic_conc', 50.0)
    >>> carrier_concentration(electron_conc=0, hole_conc=1600, intrinsic_conc=200)
    ('electron_conc', 25.0)
    >>> carrier_concentration(electron_conc=1000, hole_conc=0, intrinsic_conc=1200)
    ('hole_conc', 1440.0)
    >>> carrier_concentration(electron_conc=1000, hole_conc=400, intrinsic_conc=1200)
    Traceback (most recent call last):
        ...
    ValueError: You cannot supply more or less than 2 values
    >>> carrier_concentration(electron_conc=-1000, hole_conc=0, intrinsic_conc=1200)
    Traceback (most recent call last):
        ...
    ValueError: Electron concentration cannot be negative in a semiconductor
    >>> carrier_concentration(electron_conc=0, hole_conc=-400, intrinsic_conc=1200)
    Traceback (most recent call last):
        ...
    ValueError: Hole concentration cannot be negative in a semiconductor
    >>> carrier_concentration(electron_conc=0, hole_conc=400, intrinsic_conc=-1200)
    Traceback (most recent call last):
        ...
    ValueError: Intrinsic concentration cannot be negative in a semiconductor
    """
    if (electron_conc, hole_conc, intrinsic_conc).count(0) != 1:
        raise ValueError("You cannot supply more or less than 2 values")
    elif electron_conc < 0:
        raise ValueError("Electron concentration cannot be negative in a semiconductor")
    elif hole_conc < 0:
        raise ValueError("Hole concentration cannot be negative in a semiconductor")
    elif intrinsic_conc < 0:
        raise ValueError(
            "Intrinsic concentration cannot be negative in a semiconductor"
        )
    elif electron_conc == 0:
        return ("electron_conc", intrinsic_conc**2 / hole_conc)
    elif hole_conc == 0:
        return ("hole_conc", intrinsic_conc**2 / electron_conc)
    elif intrinsic_conc == 0:
        return ("intrinsic_conc", (electron_conc * hole_conc) ** 0.5)
    else:
        return (-1, -1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
