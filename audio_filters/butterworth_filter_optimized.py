"""
Butterworth Filter — Optimized Variants & Benchmark

Variant 1: scipy.signal.butter — Direct coefficient generation using SciPy
Variant 2: Precomputed trig — Cache sin/cos for repeated filter creation
Variant 3: Cascaded biquads — Higher-order Butterworth via cascaded 2nd-order sections

Original: Audio EQ Cookbook formulas with manual trig computation.
"""

from __future__ import annotations

import time
from math import cos, sin, sqrt, tau

import numpy as np


# ── Original: Audio EQ Cookbook ───────────────────────────────────────────────

def original_lowpass(
    frequency: int, samplerate: int, q_factor: float = 1 / sqrt(2)
) -> tuple[list[float], list[float]]:
    """
    Original lowpass using Audio EQ Cookbook formulas.
    Returns (a_coeffs, b_coeffs).

    >>> a, b = original_lowpass(1000, 48000)
    >>> round(a[0], 6)
    1.092296
    """
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = (1 - _cos) / 2
    b1 = 1 - _cos
    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    return [a0, a1, a2], [b0, b1, b0]


def original_highpass(
    frequency: int, samplerate: int, q_factor: float = 1 / sqrt(2)
) -> tuple[list[float], list[float]]:
    """
    Original highpass.

    >>> a, b = original_highpass(1000, 48000)
    >>> round(b[0], 6)
    0.995722
    """
    w0 = tau * frequency / samplerate
    _sin = sin(w0)
    _cos = cos(w0)
    alpha = _sin / (2 * q_factor)

    b0 = (1 + _cos) / 2
    b1 = -1 - _cos
    a0 = 1 + alpha
    a1 = -2 * _cos
    a2 = 1 - alpha

    return [a0, a1, a2], [b0, b1, b0]


# ── Variant 1: SciPy butter ─────────────────────────────────────────────────

def scipy_lowpass(
    frequency: int, samplerate: int, order: int = 2
) -> tuple[np.ndarray, np.ndarray]:
    """
    SciPy's optimized Butterworth design. Supports arbitrary order.

    >>> b, a = scipy_lowpass(1000, 48000)
    >>> len(a) == 3
    True
    """
    from scipy.signal import butter

    b, a = butter(order, frequency, btype="low", fs=samplerate)
    return b, a


def scipy_highpass(
    frequency: int, samplerate: int, order: int = 2
) -> tuple[np.ndarray, np.ndarray]:
    """
    SciPy highpass Butterworth design.

    >>> b, a = scipy_highpass(1000, 48000)
    >>> len(a) == 3
    True
    """
    from scipy.signal import butter

    b, a = butter(order, frequency, btype="high", fs=samplerate)
    return b, a


# ── Variant 2: Precomputed Trig Factory ─────────────────────────────────────

class ButterworthFactory:
    """
    Factory that precomputes trig values for a given frequency/samplerate,
    enabling fast creation of multiple filter types at the same frequency.

    >>> factory = ButterworthFactory(1000, 48000)
    >>> a, b = factory.lowpass()
    >>> round(a[0], 6)
    1.092296
    """

    def __init__(
        self, frequency: int, samplerate: int,
        q_factor: float = 1 / sqrt(2)
    ) -> None:
        self.w0 = tau * frequency / samplerate
        self._sin = sin(self.w0)
        self._cos = cos(self.w0)
        self.alpha = self._sin / (2 * q_factor)

    def lowpass(self) -> tuple[list[float], list[float]]:
        b0 = (1 - self._cos) / 2
        b1 = 1 - self._cos
        a0 = 1 + self.alpha
        a1 = -2 * self._cos
        a2 = 1 - self.alpha
        return [a0, a1, a2], [b0, b1, b0]

    def highpass(self) -> tuple[list[float], list[float]]:
        b0 = (1 + self._cos) / 2
        b1 = -1 - self._cos
        a0 = 1 + self.alpha
        a1 = -2 * self._cos
        a2 = 1 - self.alpha
        return [a0, a1, a2], [b0, b1, b0]

    def bandpass(self) -> tuple[list[float], list[float]]:
        b0 = self._sin / 2
        b2 = -b0
        a0 = 1 + self.alpha
        a1 = -2 * self._cos
        a2 = 1 - self.alpha
        return [a0, a1, a2], [b0, 0.0, b2]

    def allpass(self) -> tuple[list[float], list[float]]:
        b0 = 1 - self.alpha
        b1 = -2 * self._cos
        b2 = 1 + self.alpha
        return [b2, b1, b0], [b0, b1, b2]


# ── Variant 3: Cascaded Biquad Sections (SOS) ───────────────────────────────

def cascaded_sos_lowpass(
    frequency: int, samplerate: int, order: int = 4
) -> np.ndarray:
    """
    Higher-order Butterworth via second-order sections (SOS).
    More numerically stable than transfer function form for order > 2.

    Returns SOS array of shape (n_sections, 6): [b0,b1,b2,a0,a1,a2] per section.

    >>> sos = cascaded_sos_lowpass(1000, 48000, 4)
    >>> sos.shape[1]
    6
    >>> sos.shape[0]
    2
    """
    from scipy.signal import butter

    sos = butter(order, frequency, btype="low", fs=samplerate, output="sos")
    return sos


def apply_sos(sos: np.ndarray, signal: np.ndarray) -> np.ndarray:
    """
    Apply cascaded SOS filter to a signal.

    >>> sos = cascaded_sos_lowpass(1000, 48000, 4)
    >>> out = apply_sos(sos, np.array([1.0, 0.0, 0.0, 0.0]))
    >>> len(out) == 4
    True
    """
    from scipy.signal import sosfilt

    return sosfilt(sos, signal)


# ── Benchmark ────────────────────────────────────────────────────────────────

def benchmark(n_iterations: int = 10_000) -> None:
    """Benchmark filter coefficient design speed across variants."""
    freq, sr = 1000, 48000

    results = {}

    # Original
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        original_lowpass(freq, sr)
    results["original_cookbook"] = time.perf_counter() - t0

    # SciPy butter
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        scipy_lowpass(freq, sr)
    results["scipy_butter"] = time.perf_counter() - t0

    # Precomputed trig factory
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        factory = ButterworthFactory(freq, sr)
        factory.lowpass()
    results["precomputed_trig"] = time.perf_counter() - t0

    # Precomputed factory — multiple filter types from one factory
    t0 = time.perf_counter()
    for _ in range(n_iterations):
        factory = ButterworthFactory(freq, sr)
        factory.lowpass()
        factory.highpass()
        factory.bandpass()
        factory.allpass()
    results["factory_4_types"] = time.perf_counter() - t0

    # Verify coefficients match
    a_orig, b_orig = original_lowpass(freq, sr)
    b_scipy, a_scipy = scipy_lowpass(freq, sr)
    factory = ButterworthFactory(freq, sr)
    a_fact, b_fact = factory.lowpass()

    max_diff_scipy = max(
        abs(a - b) for a, b in zip(a_orig + b_orig, a_scipy.tolist() + b_scipy.tolist())
    )
    max_diff_fact = max(abs(a - b) for a, b in zip(a_orig + b_orig, a_fact + b_fact))

    print(f"Butterworth Filter Design Benchmark ({n_iterations:,} iterations)")
    print("=" * 60)
    fastest = min(results.values())
    for name, elapsed in sorted(results.items(), key=lambda x: x[1]):
        ratio = elapsed / fastest
        per_iter = elapsed / n_iterations * 1_000_000
        print(f"  {name:22s}: {elapsed:.4f}s ({ratio:.1f}x, {per_iter:.1f}us/iter)")

    print(f"\nCoefficient match (max abs diff vs original):")
    print(f"  scipy_butter:     {max_diff_scipy:.2e}")
    print(f"  precomputed_trig: {max_diff_fact:.2e}")

    # Bonus: signal processing speed comparison
    print(f"\n--- Signal Processing Speed (100k samples) ---")
    from scipy.signal import lfilter, sosfilt

    np.random.seed(42)
    sig = np.random.uniform(-1.0, 1.0, 100_000)

    b_sp, a_sp = scipy_lowpass(freq, sr)
    t0 = time.perf_counter()
    lfilter(b_sp, a_sp, sig)
    t_lfilter = time.perf_counter() - t0

    sos = cascaded_sos_lowpass(freq, sr, 4)
    t0 = time.perf_counter()
    sosfilt(sos, sig)
    t_sos = time.perf_counter() - t0

    print(f"  scipy lfilter (order 2):  {t_lfilter:.4f}s")
    print(f"  scipy sosfilt (order 4):  {t_sos:.4f}s")


if __name__ == "__main__":
    benchmark()
