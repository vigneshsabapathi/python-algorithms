"""
Filter Frequency & Phase Response — Pure Math (No GUI)

Computes the frequency response (magnitude in dB) and phase response (radians)
of any digital filter using FFT of the impulse response.

Method:
    1. Generate impulse: [1, 0, 0, ..., 0]
    2. Pass through filter to get impulse response h[n]
    3. Zero-pad to samplerate length for frequency resolution
    4. FFT -> magnitude (dB) and phase (radians)

TheAlgorithms source:
    https://github.com/TheAlgorithms/Python/blob/master/audio_filters/show_response.py
    (matplotlib visualization removed; pure math computation retained)
"""

from __future__ import annotations

from math import pi
from typing import Protocol


class FilterType(Protocol):
    """Protocol for any filter with a process(sample) -> float method."""

    def process(self, sample: float) -> float:
        """
        Calculate y[n] for a given input sample.

        >>> issubclass(FilterType, Protocol)
        True
        """
        ...


def get_impulse_response(
    filter_type: FilterType, size: int = 512
) -> list[float]:
    """
    Compute the impulse response of a filter by feeding a unit impulse.

    Args:
        filter_type: any object with a process(sample) method
        size: number of impulse response samples

    Returns:
        list of impulse response values h[n]

    >>> from audio_filters.iir_filter import IIRFilter
    >>> filt = IIRFilter(1)
    >>> filt.set_coefficients([1.0, 0.0], [1.0, 0.0])
    >>> get_impulse_response(filt, 4)
    [1.0, 0.0, 0.0, 0.0]

    >>> filt = IIRFilter(1)
    >>> filt.set_coefficients([1.0, -0.5], [1.0, 0.0])
    >>> resp = get_impulse_response(filt, 4)
    >>> [round(x, 4) for x in resp]
    [1.0, 0.5, 0.25, 0.125]
    """
    inputs = [1.0] + [0.0] * (size - 1)
    return [filter_type.process(sample) for sample in inputs]


def compute_frequency_response_db(
    filter_type: FilterType,
    samplerate: int,
    size: int = 512,
) -> tuple[list[float], list[float]]:
    """
    Compute the frequency response magnitude in dB.

    Args:
        filter_type: any filter with process() method
        samplerate: sample rate in Hz
        size: impulse response length before zero-padding

    Returns:
        (frequencies_hz, magnitude_db) — both lists of length samplerate//2

    >>> from audio_filters.iir_filter import IIRFilter
    >>> filt = IIRFilter(2)
    >>> freqs, mag_db = compute_frequency_response_db(filt, 1000, 64)
    >>> len(freqs) == 500
    True
    >>> abs(mag_db[1] - 0.0) < 0.01  # passthrough filter ≈ 0 dB
    True
    """
    import numpy as np

    outputs = get_impulse_response(filter_type, size)

    # Zero-pad to samplerate for 1 Hz resolution
    filler = [0.0] * (samplerate - size)
    outputs += filler

    fft_out = np.abs(np.fft.fft(outputs))
    # Avoid log(0) by clamping to a tiny value
    fft_out = np.maximum(fft_out, 1e-12)
    fft_db = 20 * np.log10(fft_out)

    nyquist = samplerate // 2
    freqs = list(range(nyquist))
    mag_db = fft_db[:nyquist].tolist()

    return freqs, mag_db


def compute_phase_response(
    filter_type: FilterType,
    samplerate: int,
    size: int = 512,
) -> tuple[list[float], list[float]]:
    """
    Compute the phase response in radians (unwrapped).

    Args:
        filter_type: any filter with process() method
        samplerate: sample rate in Hz
        size: impulse response length before zero-padding

    Returns:
        (frequencies_hz, phase_radians) — both lists of length samplerate//2

    >>> from audio_filters.iir_filter import IIRFilter
    >>> filt = IIRFilter(2)
    >>> freqs, phase = compute_phase_response(filt, 1000, 64)
    >>> len(freqs) == 500
    True
    >>> abs(phase[0]) < 0.01  # DC phase ≈ 0 for passthrough
    True
    """
    import numpy as np

    outputs = get_impulse_response(filter_type, size)

    filler = [0.0] * (samplerate - size)
    outputs += filler

    fft_out = np.angle(np.fft.fft(outputs))
    unwrapped = np.unwrap(fft_out, -2 * pi)

    nyquist = samplerate // 2
    freqs = list(range(nyquist))
    phase = unwrapped[:nyquist].tolist()

    return freqs, phase


def get_bounds(
    fft_results: list[float], samplerate: int
) -> tuple[float, float]:
    """
    Get reasonable display bounds for frequency response plot.

    >>> get_bounds([0.0, -30.0, 5.0, 10.0, -10.0, -25.0, 0.0, 0.0], 16)
    (-30.0, 20)
    >>> get_bounds([0.0, 0.0, 0.0, 0.0], 8)
    (-20, 20)
    """
    # Skip DC bin (index 0), look at bins 1..nyquist-1
    nyquist = samplerate // 2
    relevant = fft_results[1 : nyquist - 1] if len(fft_results) >= nyquist else fft_results
    if not relevant:
        return (-20, 20)
    lowest = min(-20, min(relevant))
    highest = max(20, max(relevant))
    return lowest, highest


def summarize_response(
    filter_type: FilterType, samplerate: int, size: int = 512
) -> dict:
    """
    Compute a summary of the filter's frequency response.

    Returns dict with dc_gain_db, nyquist_gain_db, peak_gain_db,
    peak_freq_hz, and bounds.

    >>> from audio_filters.iir_filter import IIRFilter
    >>> filt = IIRFilter(2)
    >>> summary = summarize_response(filt, 48000)
    >>> abs(summary['dc_gain_db']) < 0.01
    True
    >>> summary['peak_freq_hz'] >= 0
    True
    """
    freqs, mag_db = compute_frequency_response_db(filter_type, samplerate, size)

    peak_idx = max(range(len(mag_db)), key=lambda i: mag_db[i])

    return {
        "dc_gain_db": round(mag_db[0], 4),
        "nyquist_gain_db": round(mag_db[-1], 4),
        "peak_gain_db": round(mag_db[peak_idx], 4),
        "peak_freq_hz": freqs[peak_idx],
        "bounds": get_bounds(mag_db, samplerate),
    }


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
