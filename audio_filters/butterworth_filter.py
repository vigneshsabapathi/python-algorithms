"""
Butterworth IIR Filter Design — 2nd-Order Audio EQ Cookbook Filters

Creates standard 2nd-order IIR filters using the Butterworth design method.
Butterworth filters have maximally flat magnitude response in the passband.

Supported filter types:
    - Lowpass, Highpass, Bandpass, Allpass
    - Peak (parametric EQ), Low-shelf, High-shelf

Design equations from:
    https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html

TheAlgorithms source:
    https://github.com/TheAlgorithms/Python/blob/master/audio_filters/butterworth_filter.py

Alternatively use scipy.signal.butter for equivalent results.
"""

from math import cos, sin, sqrt, tau

from audio_filters.iir_filter import IIRFilter


def make_lowpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    Create a 2nd-order Butterworth low-pass filter.

    Args:
        frequency: cutoff frequency in Hz
        samplerate: sample rate in Hz
        q_factor: quality factor (default 1/sqrt(2) for Butterworth)

    Returns:
        Configured IIRFilter instance

    >>> filt = make_lowpass(1000, 48000)
    >>> filt.a_coeffs + filt.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.004277569313094809,
     0.008555138626189618, 0.004277569313094809]

    >>> filt = make_lowpass(4000, 44100, 0.5)
    >>> len(filt.a_coeffs)
    3

    >>> make_lowpass(0, 48000)
    Traceback (most recent call last):
        ...
    ValueError: Frequency must be positive and less than Nyquist (24000 Hz), got 0

    >>> make_lowpass(25000, 48000)
    Traceback (most recent call last):
        ...
    ValueError: Frequency must be positive and less than Nyquist (24000 Hz), got 25000
    """
    _validate_frequency(frequency, samplerate)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = (1 - _cos) / 2
    b1 = 1 - _cos

    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b0])
    return filt


def make_highpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    Create a 2nd-order Butterworth high-pass filter.

    >>> filt = make_highpass(1000, 48000)
    >>> filt.a_coeffs + filt.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.9957224306869052,
     -1.9914448613738105, 0.9957224306869052]
    """
    _validate_frequency(frequency, samplerate)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = (1 + _cos) / 2
    b1 = -1 - _cos

    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b0])
    return filt


def make_bandpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    Create a 2nd-order Butterworth band-pass filter.

    >>> filt = make_bandpass(1000, 48000)
    >>> filt.a_coeffs + filt.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.06526309611002579,
     0, -0.06526309611002579]
    """
    _validate_frequency(frequency, samplerate)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = _sin / 2
    b1 = 0
    b2 = -b0

    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_allpass(
    frequency: int,
    samplerate: int,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    Create a 2nd-order all-pass filter (passes all frequencies, shifts phase).

    >>> filt = make_allpass(1000, 48000)
    >>> filt.a_coeffs + filt.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0922959556412573, -1.9828897227476208, 0.9077040443587427, 0.9077040443587427,
     -1.9828897227476208, 1.0922959556412573]
    """
    _validate_frequency(frequency, samplerate)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = 1 - alpha
    b1 = -2 * _cos
    b2 = 1 + alpha

    filt = IIRFilter(2)
    filt.set_coefficients([b2, b1, b0], [b0, b1, b2])
    return filt


def make_peak(
    frequency: int,
    samplerate: int,
    gain_db: float,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    Create a 2nd-order peak (parametric EQ) filter.

    >>> filt = make_peak(1000, 48000, 6)
    >>> filt.a_coeffs + filt.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [1.0653405327119334, -1.9828897227476208, 0.9346594672880666, 1.1303715025601122,
     -1.9828897227476208, 0.8696284974398878]
    """
    _validate_frequency(frequency, samplerate)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)
    big_a = 10 ** (gain_db / 40)

    b0 = 1 + alpha * big_a
    b1 = -2 * _cos
    b2 = 1 - alpha * big_a
    a0 = 1 + alpha / big_a
    a1 = -2 * _cos
    a2 = 1 - alpha / big_a

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_lowshelf(
    frequency: int,
    samplerate: int,
    gain_db: float,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    Create a 2nd-order low-shelf filter.

    >>> filt = make_lowshelf(1000, 48000, 6)
    >>> filt.a_coeffs + filt.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [3.0409336710888786, -5.608870992220748, 2.602157875636628, 3.139954022810743,
     -5.591841778072785, 2.5201667380627257]
    """
    _validate_frequency(frequency, samplerate)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)
    big_a = 10 ** (gain_db / 40)
    pmc = (big_a + 1) - (big_a - 1) * _cos
    ppmc = (big_a + 1) + (big_a - 1) * _cos
    mpc = (big_a - 1) - (big_a + 1) * _cos
    pmpc = (big_a - 1) + (big_a + 1) * _cos
    aa2 = 2 * sqrt(big_a) * alpha

    b0 = big_a * (pmc + aa2)
    b1 = 2 * big_a * mpc
    b2 = big_a * (pmc - aa2)
    a0 = ppmc + aa2
    a1 = -2 * pmpc
    a2 = ppmc - aa2

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def make_highshelf(
    frequency: int,
    samplerate: int,
    gain_db: float,
    q_factor: float = 1 / sqrt(2),
) -> IIRFilter:
    """
    Create a 2nd-order high-shelf filter.

    >>> filt = make_highshelf(1000, 48000, 6)
    >>> filt.a_coeffs + filt.b_coeffs  # doctest: +NORMALIZE_WHITESPACE
    [2.2229172136088806, -3.9587208137297303, 1.7841414181566304, 4.295432981120543,
     -7.922740859457287, 3.6756456963725253]
    """
    _validate_frequency(frequency, samplerate)
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)
    big_a = 10 ** (gain_db / 40)
    pmc = (big_a + 1) - (big_a - 1) * _cos
    ppmc = (big_a + 1) + (big_a - 1) * _cos
    mpc = (big_a - 1) - (big_a + 1) * _cos
    pmpc = (big_a - 1) + (big_a + 1) * _cos
    aa2 = 2 * sqrt(big_a) * alpha

    b0 = big_a * (ppmc + aa2)
    b1 = -2 * big_a * pmpc
    b2 = big_a * (ppmc - aa2)
    a0 = pmc + aa2
    a1 = 2 * mpc
    a2 = pmc - aa2

    filt = IIRFilter(2)
    filt.set_coefficients([a0, a1, a2], [b0, b1, b2])
    return filt


def _validate_frequency(frequency: int, samplerate: int) -> None:
    """
    Validate that frequency is within valid range (0, Nyquist).

    >>> _validate_frequency(1000, 48000)  # valid — no error

    >>> _validate_frequency(0, 48000)
    Traceback (most recent call last):
        ...
    ValueError: Frequency must be positive and less than Nyquist (24000 Hz), got 0

    >>> _validate_frequency(24000, 48000)
    Traceback (most recent call last):
        ...
    ValueError: Frequency must be positive and less than Nyquist (24000 Hz), got 24000
    """
    nyquist = samplerate // 2
    if frequency <= 0 or frequency >= nyquist:
        raise ValueError(
            f"Frequency must be positive and less than Nyquist "
            f"({nyquist} Hz), got {frequency}"
        )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
