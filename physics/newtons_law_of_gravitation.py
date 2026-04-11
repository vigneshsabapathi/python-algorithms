"""
Newton's Law of Universal Gravitation.

    F = G * m1 * m2 / r^2

where:
    G  = gravitational constant (6.674e-11 m^3 kg^-1 s^-2)
    m1 = mass of first body (kg)
    m2 = mass of second body (kg)
    r  = distance between centers of mass (m)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/newtons_law_of_gravitation.py
"""

G = 6.674e-11  # gravitational constant


def gravitational_force(mass1: float, mass2: float, distance: float) -> float:
    """
    Calculate the gravitational force between two masses.

    >>> gravitational_force(5.972e24, 7.348e22, 3.844e8)
    1.982e+20
    >>> gravitational_force(100, 100, 1)
    6.674e-07
    >>> gravitational_force(1, 1, 0)
    Traceback (most recent call last):
        ...
    ValueError: distance must be positive
    >>> gravitational_force(-1, 1, 1)
    Traceback (most recent call last):
        ...
    ValueError: masses must be positive
    """
    if mass1 <= 0 or mass2 <= 0:
        raise ValueError("masses must be positive")
    if distance <= 0:
        raise ValueError("distance must be positive")

    force = G * mass1 * mass2 / distance**2
    return float(f"{force:.3e}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
