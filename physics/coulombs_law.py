"""
Coulomb's Law.

Coulomb's Law describes the electrostatic force between two charged particles:
    F = k * |q1 * q2| / r^2

where:
    k  = Coulomb's constant (8.9875517873681764e9 N*m^2/C^2)
    q1 = charge of first particle (C)
    q2 = charge of second particle (C)
    r  = distance between the charges (m)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/coulombs_law.py
"""

COULOMBS_CONSTANT = 8.9875517873681764e9  # N*m^2/C^2


def coulombs_law(charge1: float, charge2: float, distance: float) -> float:
    """
    Calculate the electrostatic force between two charges.

    >>> coulombs_law(1e-6, 1e-6, 1)
    0.009
    >>> coulombs_law(1e-6, -1e-6, 1)
    -0.009
    >>> coulombs_law(2e-6, 3e-6, 0.5)
    0.216
    >>> coulombs_law(1, 1, 0)
    Traceback (most recent call last):
        ...
    ValueError: distance must be positive
    """
    if distance <= 0:
        raise ValueError("distance must be positive")

    force = COULOMBS_CONSTANT * charge1 * charge2 / distance**2
    return round(force, 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
