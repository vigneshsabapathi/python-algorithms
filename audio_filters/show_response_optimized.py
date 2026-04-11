"""
Filter Frequency Response — Optimized Variants & Benchmark

Variant 1: NumPy vectorized FFT (full numpy pipeline, no Python loops)
Variant 2: scipy.signal.freqz (direct z-transform evaluation, no impulse needed)
Variant 3: Analytic Butterworth magnitude (closed-form, no FFT at all)

Original: Impulse response -> zero-pad -> FFT -> magnitude in dB.
"""

from __future__ import annotations

import time
from math import cos, pi, sqrt, tau

import numpy as np


# ── Original: Impulse-based FFT response ─────────────────────────────────────

def original_frequency_response(
    a_coeffs: list[float],
    b_coeffs: list[float],
    samplerate: int,
    size: int = 512,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute frequency response via impulse -> IIR process -> FFT.
    Returns (frequencies, magnitude_db) up to Nyquist.

    >>> freqs, mag = original_frequency_response([1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 1000)
    >>> abs(mag[1]) < 0.01  # passthrough
    True
    """
    from audio_filters.iir_filter import IIRFilter

    order = len(a_coeffs) - 1
    filt = IIRFilter(order)
    filt.set_coefficients(a_coeffs, b_coeffs)

    inputs = [1.0] + [0.0] * (size - 1)
    outputs = [filt.process(s) for s in inputs]
    outputs += [0.0] * (samplerate - size)

    fft_out = np.abs(np.fft.fft(outputs))
    fft_out = np.maximum(fft_out, 1e-12)
    fft_db = 20 * np.log10(fft_out)

    nyquist = samplerate // 2
    freqs = np.arange(nyquist)
    return freqs, fft_db[:nyquist]


# ── Variant 1: Full NumPy Pipeline ──────────────────────────────────────────

def numpy_frequency_response(
    a_coeffs: list[float],
    b_coeffs: list[float],
    samplerate: int,
    n_points: int = 4096,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute frequency response using scipy.signal.lfilter + numpy FFT.
    Avoids Python-level sample loop entirely.

    >>> freqs, mag = numpy_frequency_response([1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 1000)
    >>> abs(mag[1]) < 0.01
    True
    """
    from scipy.signal import lfilter

    # Generate impulse in numpy
    impulse = np.zeros(n_points)
    impulse[0] = 1.0

    # Filter with C-optimized lfilter
    h = lfilter(b_coeffs, a_coeffs, impulse)

    # Zero-pad to samplerate
    if len(h) < samplerate:
        h = np.concatenate([h, np.zeros(samplerate - len(h))])

    fft_out = np.abs(np.fft.fft(h))
    fft_out = np.maximum(fft_out, 1e-12)
    fft_db = 20 * np.log10(fft_out)

    nyquist = samplerate // 2
    freqs = np.arange(nyquist)
    return freqs, fft_db[:nyquist]


# ── Variant 2: scipy.signal.freqz (direct z-transform) ──────────────────────

def scipy_freqz_response(
    a_coeffs: list[float],
    b_coeffs: list[float],
    samplerate: int,
    n_points: int = 4096,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Evaluate transfer function H(z) directly on the unit circle using freqz.
    No impulse response or zero-padding needed — most accurate method.

    >>> freqs, mag = scipy_freqz_response([1.0, 0.0, 0.0], [1.0, 0.0, 0.0], 1000)
    >>> abs(mag[0]) < 0.01  # DC gain of passthrough
    True
    """
    from scipy.signal import freqz

    w, h = freqz(b_coeffs, a_coeffs, worN=n_points, fs=samplerate)
    mag = np.abs(h)
    mag = np.maximum(mag, 1e-12)
    mag_db = 20 * np.log10(mag)

    return w, mag_db


# ── Variant 3: Analytic Butterworth Magnitude ────────────────────────────────

def analytic_butterworth_response(
    cutoff_freq: float,
    samplerate: int,
    order: int = 2,
    n_points: int = 4096,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Closed-form Butterworth magnitude response (analog approximation).
    |H(jw)|^2 = 1 / (1 + (f/fc)^(2*N))

    No FFT, no filter object — pure math. Fastest for Butterworth specifically.

    >>> freqs, mag = analytic_butterworth_response(1000, 48000)
    >>> abs(mag[0]) < 0.01  # DC = 0 dB
    True
    >>> mag[-1] < -10  # well below cutoff
    True
    """
    freqs = np.linspace(0, samplerate / 2, n_points, endpoint=False)
    # Avoid division by zero at DC
    ratio = freqs / cutoff_freq
    magnitude_sq = 1.0 / (1.0 + ratio ** (2 * order))
    magnitude_sq = np.maximum(magnitude_sq, 1e-24)
    mag_db = 10 * np.log10(magnitude_sq)

    return freqs, mag_db


# ── Benchmark ────────────────────────────────────────────────────────────────

def benchmark(n_iterations: int = 100) -> None:
    """Benchmark frequency response computation methods."""
    # 2nd-order Butterworth lowpass 1kHz @ 48kHz
    a = [1.0922959556412573, -1.9828897227476208, 0.9077040443587427]
    b = [0.004277569313094809, 0.008555138626189618, 0.004277569313094809]
    sr = 48000

    results = {}

    # Original (impulse + Python loop + FFT)
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        original_frequency_response(a, b, sr)
    results["original_impulse"] = time.perf_counter() - t0

    # Variant 1: NumPy pipeline
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        numpy_frequency_response(a, b, sr)
    results["numpy_lfilter_fft"] = time.perf_counter() - t0

    # Variant 2: scipy.signal.freqz
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        scipy_freqz_response(a, b, sr)
    results["scipy_freqz"] = time.perf_counter() - t0

    # Variant 3: Analytic
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        analytic_butterworth_response(1000, sr)
    results["analytic_closed"] = time.perf_counter() - t0

    # Verify at key frequencies
    _, mag_orig = original_frequency_response(a, b, sr)
    _, mag_np = numpy_frequency_response(a, b, sr)
    w_fz, mag_fz = scipy_freqz_response(a, b, sr)
    _, mag_an = analytic_butterworth_response(1000, sr)

    print(f"Frequency Response Benchmark ({n_iterations} iterations)")
    print("=" * 60)
    fastest = min(results.values())
    for name, elapsed in sorted(results.items(), key=lambda x: x[1]):
        ratio = elapsed / fastest
        per_iter = elapsed / n_iterations * 1000
        print(f"  {name:22s}: {elapsed:.4f}s ({ratio:.1f}x, {per_iter:.1f}ms/iter)")

    # Compare at cutoff frequency (1kHz)
    print(f"\nGain at 1kHz cutoff (should be ~-3.01 dB):")
    print(f"  original:   {mag_orig[1000]:.2f} dB")
    print(f"  numpy:      {mag_np[1000]:.2f} dB")
    # freqz uses different freq axis, find closest to 1kHz
    idx_1k = np.argmin(np.abs(w_fz - 1000))
    print(f"  freqz:      {mag_fz[idx_1k]:.2f} dB")
    idx_1k_an = int(1000 / (sr / 2) * len(mag_an))
    print(f"  analytic:   {mag_an[idx_1k_an]:.2f} dB")


if __name__ == "__main__":
    benchmark()
