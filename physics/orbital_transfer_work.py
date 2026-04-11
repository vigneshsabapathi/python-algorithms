"""
Orbital Transfer Work (Hohmann Transfer).

The work required to transfer a satellite from one circular orbit to another
via a Hohmann transfer ellipse.

    W = -G*M*m/2 * (1/r2 - 1/r1)

The total delta-v for a Hohmann transfer:
    dv1 = sqrt(G*M/r1) * (sqrt(2*r2/(r1+r2)) - 1)
    dv2 = sqrt(G*M/r2) * (1 - sqrt(2*r1/(r1+r2)))

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/orbital_transfer_work.py
"""

from math import sqrt

G = 6.674e-11  # gravitational constant


def hohmann_transfer_work(
    central_mass: float,
    satellite_mass: float,
    initial_radius: float,
    final_radius: float,
) -> float:
    """
    Calculate the work done in a Hohmann transfer between two circular orbits.

    >>> round(hohmann_transfer_work(5.972e24, 1000, 6.671e6, 4.2164e7), 2)
    25146987706.21
    >>> hohmann_transfer_work(5.972e24, 1000, 0, 4.2164e7)
    Traceback (most recent call last):
        ...
    ValueError: radii must be positive
    >>> hohmann_transfer_work(-1, 1000, 1e7, 2e7)
    Traceback (most recent call last):
        ...
    ValueError: central_mass must be positive
    """
    if central_mass <= 0:
        raise ValueError("central_mass must be positive")
    if satellite_mass <= 0:
        raise ValueError("satellite_mass must be positive")
    if initial_radius <= 0 or final_radius <= 0:
        raise ValueError("radii must be positive")

    # Work = change in orbital energy
    # E = -G*M*m / (2*r)
    return -G * central_mass * satellite_mass / 2 * (
        1 / final_radius - 1 / initial_radius
    )


def hohmann_delta_v(
    central_mass: float,
    initial_radius: float,
    final_radius: float,
) -> tuple[float, float, float]:
    """
    Calculate delta-v values for a Hohmann transfer.
    Returns (dv1, dv2, total_dv).

    >>> dv1, dv2, total = hohmann_delta_v(5.972e24, 6.671e6, 4.2164e7)
    >>> round(total, 2)
    3895.19
    """
    if central_mass <= 0:
        raise ValueError("central_mass must be positive")
    if initial_radius <= 0 or final_radius <= 0:
        raise ValueError("radii must be positive")

    v1 = sqrt(G * central_mass / initial_radius)
    v2 = sqrt(G * central_mass / final_radius)

    r_sum = initial_radius + final_radius

    dv1 = v1 * (sqrt(2 * final_radius / r_sum) - 1)
    dv2 = v2 * (1 - sqrt(2 * initial_radius / r_sum))

    return (abs(dv1), abs(dv2), abs(dv1) + abs(dv2))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
