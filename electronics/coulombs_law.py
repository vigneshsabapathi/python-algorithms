#!/usr/bin/env python3
"""
Coulomb's Law — electrostatic force between two point charges.

F = k * |q1 * q2| / r^2
Reference: https://en.wikipedia.org/wiki/Coulomb%27s_law

Run:
    python -m doctest electronics/coulombs_law.py -v
"""

from __future__ import annotations

COULOMBS_CONSTANT = 8.988e9  # units = N * m^2 * C^-2


def couloumbs_law(
    force: float, charge1: float, charge2: float, distance: float
) -> dict[str, float]:
    """
    Apply Coulomb's Law on any three given values (set the unknown to 0).

    >>> couloumbs_law(force=0, charge1=3, charge2=5, distance=2000)
    {'force': 33705.0}
    >>> couloumbs_law(force=10, charge1=3, charge2=5, distance=0)
    {'distance': 116112.01488218177}
    >>> couloumbs_law(force=10, charge1=0, charge2=5, distance=2000)
    {'charge1': 0.0008900756564307966}
    >>> couloumbs_law(force=0, charge1=0, charge2=5, distance=2000)
    Traceback (most recent call last):
      ...
    ValueError: One and only one argument must be 0
    >>> couloumbs_law(force=0, charge1=3, charge2=5, distance=-2000)
    Traceback (most recent call last):
      ...
    ValueError: Distance cannot be negative
    """
    charge_product = abs(charge1 * charge2)

    if (force, charge1, charge2, distance).count(0) != 1:
        raise ValueError("One and only one argument must be 0")
    if distance < 0:
        raise ValueError("Distance cannot be negative")
    if force == 0:
        force = COULOMBS_CONSTANT * charge_product / (distance**2)
        return {"force": force}
    elif charge1 == 0:
        charge1 = abs(force) * (distance**2) / (COULOMBS_CONSTANT * charge2)
        return {"charge1": charge1}
    elif charge2 == 0:
        charge2 = abs(force) * (distance**2) / (COULOMBS_CONSTANT * charge1)
        return {"charge2": charge2}
    elif distance == 0:
        distance = (COULOMBS_CONSTANT * charge_product / abs(force)) ** 0.5
        return {"distance": distance}
    raise ValueError("Exactly one argument must be 0")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
