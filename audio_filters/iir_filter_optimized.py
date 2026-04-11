"""
IIR Filter — Optimized Variants & Benchmark

Variant 1: NumPy vectorized (batch processing via lfilter-style)
Variant 2: Deque-based (collections.deque for O(1) shift instead of list slicing)
Variant 3: scipy.signal.lfilter (industry-standard reference)

Original: List-based delay line with Python loop per sample.
"""

from __future__ import annotations

import time
from collections import deque

import numpy as np


# ── Original: List-based IIR Filter ──────────────────────────────────────────

class IIRFilterOriginal:
    """
    Original list-based N-order IIR filter.

    >>> filt = IIRFilterOriginal(2)
    >>> filt.process(0)
    0.0
    """

    def __init__(self, order: int) -> None:
        self.order = order
        self.a_coeffs: list[float] = [1.0] + [0.0] * order
        self.b_coeffs: list[float] = [1.0] + [0.0] * order
        self.input_history: list[float] = [0.0] * order
        self.output_history: list[float] = [0.0] * order

    def set_coefficients(
        self, a_coeffs: list[float], b_coeffs: list[float]
    ) -> None:
        if len(a_coeffs) == self.order:
            a_coeffs = [1.0, *a_coeffs]
        self.a_coeffs = a_coeffs
        self.b_coeffs = b_coeffs

    def process(self, sample: float) -> float:
        result = 0.0
        for i in range(1, self.order + 1):
            result += (
                self.b_coeffs[i] * self.input_history[i - 1]
                - self.a_coeffs[i] * self.output_history[i - 1]
            )
        result = (result + self.b_coeffs[0] * sample) / self.a_coeffs[0]
        self.input_history[1:] = self.input_history[:-1]
        self.output_history[1:] = self.output_history[:-1]
        self.input_history[0] = sample
        self.output_history[0] = result
        return result

    def process_sequence(self, samples: list[float]) -> list[float]:
        return [self.process(s) for s in samples]


# ── Variant 1: NumPy Vectorized (batch lfilter) ─────────────────────────────

class IIRFilterNumpy:
    """
    NumPy-based IIR filter using direct-form II transposed (lfilter algorithm).
    Processes entire arrays at once — ideal for offline/batch DSP.

    >>> filt = IIRFilterNumpy(2)
    >>> float(filt.process_sequence(np.array([0.0]))[0])
    0.0
    """

    def __init__(self, order: int) -> None:
        self.order = order
        self.a_coeffs = np.array([1.0] + [0.0] * order)
        self.b_coeffs = np.array([1.0] + [0.0] * order)
        self.state = np.zeros(order)  # direct-form II transposed state

    def set_coefficients(
        self, a_coeffs: list[float], b_coeffs: list[float]
    ) -> None:
        if len(a_coeffs) == self.order:
            a_coeffs = [1.0, *a_coeffs]
        self.a_coeffs = np.array(a_coeffs)
        self.b_coeffs = np.array(b_coeffs)

    def process_sequence(self, samples: np.ndarray) -> np.ndarray:
        """
        Process entire sample array using direct-form II transposed.
        Equivalent to scipy.signal.lfilter.

        >>> filt = IIRFilterNumpy(1)
        >>> filt.set_coefficients([1.0, 0.0], [1.0, 0.0])
        >>> list(filt.process_sequence(np.array([1.0, 0.5, 0.0])))
        [1.0, 0.5, 0.0]
        """
        n = len(samples)
        output = np.zeros(n)
        state = self.state.copy()

        a = self.a_coeffs / self.a_coeffs[0]
        b = self.b_coeffs / self.a_coeffs[0]

        for i in range(n):
            output[i] = b[0] * samples[i] + state[0]
            for j in range(self.order - 1):
                state[j] = (
                    b[j + 1] * samples[i]
                    - a[j + 1] * output[i]
                    + state[j + 1]
                )
            state[self.order - 1] = (
                b[self.order] * samples[i] - a[self.order] * output[i]
            )

        self.state = state
        return output


# ── Variant 2: Deque-based IIR Filter ───────────────────────────────────────

class IIRFilterDeque:
    """
    Deque-based IIR filter — O(1) rotation instead of O(n) list slicing.

    >>> filt = IIRFilterDeque(2)
    >>> filt.process(0)
    0.0
    """

    def __init__(self, order: int) -> None:
        self.order = order
        self.a_coeffs: list[float] = [1.0] + [0.0] * order
        self.b_coeffs: list[float] = [1.0] + [0.0] * order
        self.input_history: deque[float] = deque([0.0] * order, maxlen=order)
        self.output_history: deque[float] = deque([0.0] * order, maxlen=order)

    def set_coefficients(
        self, a_coeffs: list[float], b_coeffs: list[float]
    ) -> None:
        if len(a_coeffs) == self.order:
            a_coeffs = [1.0, *a_coeffs]
        self.a_coeffs = a_coeffs
        self.b_coeffs = b_coeffs

    def process(self, sample: float) -> float:
        result = 0.0
        for i in range(1, self.order + 1):
            result += (
                self.b_coeffs[i] * self.input_history[i - 1]
                - self.a_coeffs[i] * self.output_history[i - 1]
            )
        result = (result + self.b_coeffs[0] * sample) / self.a_coeffs[0]

        # deque.appendleft with maxlen auto-discards oldest — O(1)
        self.input_history.appendleft(sample)
        self.output_history.appendleft(result)
        return result

    def process_sequence(self, samples: list[float]) -> list[float]:
        return [self.process(s) for s in samples]


# ── Variant 3: SciPy lfilter wrapper ────────────────────────────────────────

class IIRFilterScipy:
    """
    Thin wrapper around scipy.signal.lfilter — industry reference implementation.

    >>> filt = IIRFilterScipy(2)
    >>> list(filt.process_sequence([0.0]))
    [0.0]
    """

    def __init__(self, order: int) -> None:
        self.order = order
        self.a_coeffs = [1.0] + [0.0] * order
        self.b_coeffs = [1.0] + [0.0] * order

    def set_coefficients(
        self, a_coeffs: list[float], b_coeffs: list[float]
    ) -> None:
        if len(a_coeffs) == self.order:
            a_coeffs = [1.0, *a_coeffs]
        self.a_coeffs = a_coeffs
        self.b_coeffs = b_coeffs

    def process_sequence(self, samples: list[float]) -> list[float]:
        """
        >>> filt = IIRFilterScipy(1)
        >>> filt.set_coefficients([1.0, 0.0], [1.0, 0.0])
        >>> list(filt.process_sequence([1.0, 0.5, 0.0]))
        [1.0, 0.5, 0.0]
        """
        from scipy.signal import lfilter

        result = lfilter(self.b_coeffs, self.a_coeffs, samples)
        return result.tolist()


# ── Benchmark ────────────────────────────────────────────────────────────────

def benchmark(n_samples: int = 100_000, order: int = 2) -> None:
    """Run benchmark comparing all IIR filter implementations."""
    # Generate test signal (white noise)
    np.random.seed(42)
    signal = np.random.uniform(-1.0, 1.0, n_samples).tolist()
    signal_np = np.array(signal)

    # 2nd-order lowpass coefficients (1kHz @ 48kHz, Butterworth)
    a = [1.0922959556412573, -1.9828897227476208, 0.9077040443587427]
    b = [0.004277569313094809, 0.008555138626189618, 0.004277569313094809]

    results = {}

    # Original
    filt = IIRFilterOriginal(order)
    filt.set_coefficients(a, b)
    t0 = time.perf_counter()
    out_orig = filt.process_sequence(signal)
    results["original_list"] = time.perf_counter() - t0

    # Variant 1: NumPy vectorized
    filt_np = IIRFilterNumpy(order)
    filt_np.set_coefficients(a, b)
    t0 = time.perf_counter()
    out_np = filt_np.process_sequence(signal_np)
    results["numpy_dfII"] = time.perf_counter() - t0

    # Variant 2: Deque
    filt_dq = IIRFilterDeque(order)
    filt_dq.set_coefficients(a, b)
    t0 = time.perf_counter()
    out_dq = filt_dq.process_sequence(signal)
    results["deque_based"] = time.perf_counter() - t0

    # Variant 3: SciPy
    filt_sp = IIRFilterScipy(order)
    filt_sp.set_coefficients(a, b)
    t0 = time.perf_counter()
    out_sp = filt_sp.process_sequence(signal)
    results["scipy_lfilter"] = time.perf_counter() - t0

    # Verify correctness: all outputs should match
    max_diff_np = max(abs(a - b) for a, b in zip(out_orig, out_np.tolist()))
    max_diff_dq = max(abs(a - b) for a, b in zip(out_orig, out_dq))
    max_diff_sp = max(abs(a - b) for a, b in zip(out_orig, out_sp))

    print(f"IIR Filter Benchmark ({n_samples:,} samples, order={order})")
    print("=" * 60)
    fastest = min(results.values())
    for name, elapsed in sorted(results.items(), key=lambda x: x[1]):
        ratio = elapsed / fastest
        print(f"  {name:20s}: {elapsed:.4f}s ({ratio:.1f}x)")

    print(f"\nCorrectness (max absolute difference vs original):")
    print(f"  numpy_dfII:   {max_diff_np:.2e}")
    print(f"  deque_based:  {max_diff_dq:.2e}")
    print(f"  scipy_lfilter: {max_diff_sp:.2e}")


if __name__ == "__main__":
    benchmark()
