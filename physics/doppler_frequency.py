"""
Doppler Frequency Shift.

The Doppler effect describes the change in frequency of a wave in relation to
an observer moving relative to the source:
    f' = f * (v + v_observer) / (v + v_source)

where:
    f           = emitted frequency (Hz)
    v           = speed of sound / wave in medium (m/s)
    v_observer  = velocity of observer (positive = towards source)
    v_source    = velocity of source (positive = away from observer)

Reference: https://github.com/TheAlgorithms/Python/blob/master/physics/doppler_frequency.py
"""


def doppler_frequency(
    source_frequency: float,
    wave_speed: float,
    observer_velocity: float = 0.0,
    source_velocity: float = 0.0,
) -> float:
    """
    Calculate the observed frequency due to the Doppler effect.

    >>> round(doppler_frequency(440, 343, 0, 0), 2)
    440.0
    >>> round(doppler_frequency(440, 343, 30, 0), 2)
    478.48
    >>> round(doppler_frequency(440, 343, 0, 30), 2)
    404.61
    >>> round(doppler_frequency(440, 343, 30, -30), 2)
    524.35
    >>> doppler_frequency(440, 343, 0, -343)
    Traceback (most recent call last):
        ...
    ValueError: wave_speed + source_velocity must not be zero (sonic boom singularity)
    >>> doppler_frequency(-1, 343)
    Traceback (most recent call last):
        ...
    ValueError: source_frequency must be positive
    >>> doppler_frequency(440, -1)
    Traceback (most recent call last):
        ...
    ValueError: wave_speed must be positive
    """
    if source_frequency <= 0:
        raise ValueError("source_frequency must be positive")
    if wave_speed <= 0:
        raise ValueError("wave_speed must be positive")
    if wave_speed + source_velocity == 0:
        raise ValueError(
            "wave_speed + source_velocity must not be zero (sonic boom singularity)"
        )

    return source_frequency * (wave_speed + observer_velocity) / (
        wave_speed + source_velocity
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
