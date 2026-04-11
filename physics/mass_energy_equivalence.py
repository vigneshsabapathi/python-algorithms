"""
Mass-Energy Equivalence (Einstein's E=mc^2).

    E = m * c^2

where:
    E = energy (Joules)
    m = mass (kg)
    c = speed of light (299792458 m/s)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/mass_energy_equivalence.py
"""

C = 299792458  # speed of light (m/s)


def energy(mass: float) -> float:
    """
    Calculate the energy equivalent of a given mass.

    >>> energy(1)
    89875517873681764
    >>> energy(0)
    0
    >>> energy(0.001)
    89875517873681.77
    >>> energy(-1)
    Traceback (most recent call last):
        ...
    ValueError: mass must be non-negative
    """
    if mass < 0:
        raise ValueError("mass must be non-negative")

    return mass * C**2


def mass(energy_val: float) -> float:
    """
    Calculate the mass equivalent of a given energy.

    >>> round(mass(8.987551787368176e+16), 4)
    1.0
    >>> mass(0)
    0.0
    >>> mass(-1)
    Traceback (most recent call last):
        ...
    ValueError: energy must be non-negative
    """
    if energy_val < 0:
        raise ValueError("energy must be non-negative")

    return energy_val / C**2


if __name__ == "__main__":
    import doctest

    doctest.testmod()
