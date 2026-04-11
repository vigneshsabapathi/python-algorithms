"""
Photoelectric Effect.

Einstein's photoelectric equation:
    KE_max = h * f - phi

where:
    KE_max = maximum kinetic energy of emitted electrons (J)
    h      = Planck's constant (6.62607015e-34 J*s)
    f      = frequency of incident light (Hz)
    phi    = work function of the material (J)

Threshold frequency: f0 = phi / h

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/photoelectric_effect.py
"""

H = 6.62607015e-34  # Planck's constant (J*s)


def max_kinetic_energy(frequency: float, work_function: float) -> float:
    """
    Calculate the maximum kinetic energy of emitted photoelectrons.

    >>> round(max_kinetic_energy(1e15, 3e-19), 22)
    3.626e-19
    >>> max_kinetic_energy(1e14, 3e-19)  # below threshold
    Traceback (most recent call last):
        ...
    ValueError: frequency is below the threshold; no electrons emitted
    >>> max_kinetic_energy(-1, 3e-19)
    Traceback (most recent call last):
        ...
    ValueError: frequency must be positive
    >>> max_kinetic_energy(1e15, -1)
    Traceback (most recent call last):
        ...
    ValueError: work_function must be non-negative
    """
    if frequency <= 0:
        raise ValueError("frequency must be positive")
    if work_function < 0:
        raise ValueError("work_function must be non-negative")

    energy = H * frequency - work_function
    if energy < 0:
        raise ValueError("frequency is below the threshold; no electrons emitted")

    return energy


def threshold_frequency(work_function: float) -> float:
    """
    Calculate the threshold frequency for the photoelectric effect.

    >>> round(threshold_frequency(3e-19), 4)
    452757053892645.56
    >>> threshold_frequency(0)
    0.0
    """
    if work_function < 0:
        raise ValueError("work_function must be non-negative")

    return work_function / H


if __name__ == "__main__":
    import doctest

    doctest.testmod()
