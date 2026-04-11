"""
Peak signal-to-noise ratio - PSNR
    https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio

PSNR is used to measure the quality of reconstruction of lossy compression
codecs (e.g., image compression). It is the ratio between the maximum
possible power of a signal and the power of corrupting noise.

PSNR is usually expressed in decibels (dB). Higher PSNR = better quality.
Typical values for lossy image compression: 30-50 dB.

Formula:
    PSNR = 20 * log10(MAX_I / sqrt(MSE))
    MSE  = mean((original - compressed) ** 2)

This implementation works with numpy arrays or plain Python lists.
"""

from __future__ import annotations

import math


def peak_signal_to_noise_ratio(
    original: list[float] | list[list[float]],
    contrast: list[float] | list[list[float]],
) -> float:
    """
    Calculate PSNR between two signals/images represented as nested lists.

    PIXEL_MAX is assumed to be 255.0 (8-bit images).

    >>> peak_signal_to_noise_ratio([100, 100, 100], [100, 100, 100])
    100
    >>> round(peak_signal_to_noise_ratio([100, 120, 130], [110, 130, 140]), 2)
    28.13
    >>> round(peak_signal_to_noise_ratio([0, 50, 100, 150, 200], [10, 60, 110, 160, 210]), 2)
    28.13
    >>> peak_signal_to_noise_ratio([], [])
    Traceback (most recent call last):
        ...
    ValueError: Input signals must not be empty.
    """
    if not original or not contrast:
        raise ValueError("Input signals must not be empty.")

    pixel_max = 255.0

    # Flatten if nested
    flat_orig = _flatten(original)
    flat_cont = _flatten(contrast)

    if len(flat_orig) != len(flat_cont):
        raise ValueError("Signals must have the same length.")

    mse = sum((a - b) ** 2 for a, b in zip(flat_orig, flat_cont)) / len(flat_orig)

    if mse == 0:
        return 100

    return 20 * math.log10(pixel_max / math.sqrt(mse))


def _flatten(data: list) -> list[float]:
    """
    Flatten a potentially nested list into a flat list of floats.

    >>> _flatten([1, 2, 3])
    [1, 2, 3]
    >>> _flatten([[1, 2], [3, 4]])
    [1, 2, 3, 4]
    """
    result: list[float] = []
    for item in data:
        if isinstance(item, (list, tuple)):
            result.extend(_flatten(item))
        else:
            result.append(item)
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
