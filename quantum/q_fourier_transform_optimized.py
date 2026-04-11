"""
Quantum Fourier Transform — variant implementations with benchmarks.

Variants:
    1. naive_qft_recursive : Gate-by-gate recursive simulation (educational)
    2. matrix_qft          : Dense unitary matrix multiply via NumPy (baseline)
    3. classical_fft       : NumPy's FFT for comparison (not quantum, but same math)
    4. gate_sequence_qft   : Simulates the actual quantum circuit gate-by-gate

Each variant transforms a state vector of length N = 2^num_qubits.
The benchmark() function compares wall-clock time across all methods.
"""

from __future__ import annotations

import time
from typing import Callable

import numpy as np


# ---------------------------------------------------------------------------
# Variant 1 — Naive recursive QFT (Cooley-Tukey butterfly structure)
# ---------------------------------------------------------------------------

def naive_qft_recursive(state: np.ndarray) -> np.ndarray:
    """
    QFT via recursive DFT (Cooley-Tukey-style), scaled by 1/sqrt(N).

    This mirrors the classical FFT recursion but produces the QFT
    (unitary) output by normalising with 1/sqrt(N) instead of 1/N.

    >>> s = np.array([1, 0, 0, 0], dtype=complex)
    >>> r = naive_qft_recursive(s)
    >>> np.allclose(r, [0.5, 0.5, 0.5, 0.5])
    True

    >>> s2 = np.array([0, 1, 0, 0], dtype=complex)
    >>> r2 = naive_qft_recursive(s2)
    >>> np.allclose(np.abs(r2)**2, [0.25, 0.25, 0.25, 0.25])
    True
    """
    state = np.asarray(state, dtype=complex)
    n = len(state)
    if n == 1:
        return state.copy()

    even = naive_qft_recursive(state[::2])
    odd = naive_qft_recursive(state[1::2])

    omega = np.exp(2j * np.pi * np.arange(n // 2) / n)
    combined = np.empty(n, dtype=complex)
    combined[: n // 2] = even + omega * odd
    combined[n // 2 :] = even - omega * odd

    # Normalise: each recursion level contributes sqrt(2) factor,
    # so divide by sqrt(2) at each merge (total gives 1/sqrt(N)).
    return combined / np.sqrt(2)


# ---------------------------------------------------------------------------
# Variant 2 — Matrix QFT (dense unitary multiply)
# ---------------------------------------------------------------------------

def matrix_qft(state: np.ndarray) -> np.ndarray:
    """
    QFT by explicit matrix multiplication with the DFT unitary.

    >>> s = np.array([1, 0, 0, 0], dtype=complex)
    >>> r = matrix_qft(s)
    >>> np.allclose(r, [0.5, 0.5, 0.5, 0.5])
    True
    """
    state = np.asarray(state, dtype=complex)
    n = len(state)
    omega = np.exp(2j * np.pi / n)
    idx = np.arange(n)
    mat = omega ** np.outer(idx, idx) / np.sqrt(n)
    return mat @ state


# ---------------------------------------------------------------------------
# Variant 3 — Classical FFT (numpy.fft) for reference comparison
# ---------------------------------------------------------------------------

def classical_fft(state: np.ndarray) -> np.ndarray:
    """
    Classical IFFT normalised to match QFT sign convention.

    The QFT uses omega = e^{+2*pi*i/N} (positive exponent), which
    matches numpy's *inverse* FFT.  We use ifft with "ortho" norm
    to get the 1/sqrt(N) scaling that matches the QFT unitary.

    >>> s = np.array([1, 0, 0, 0], dtype=complex)
    >>> r = classical_fft(s)
    >>> np.allclose(r, [0.5, 0.5, 0.5, 0.5])
    True
    """
    return np.fft.ifft(state, norm="ortho")


# ---------------------------------------------------------------------------
# Variant 4 — Gate-sequence QFT (simulates actual quantum circuit)
# ---------------------------------------------------------------------------

def _hadamard_on_qubit(state: np.ndarray, qubit: int, num_qubits: int) -> np.ndarray:
    """Apply Hadamard gate to a specific qubit in the state vector."""
    n = 2**num_qubits
    h = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    # Build full operator via tensor product: I x ... x H x ... x I
    op = np.eye(1, dtype=complex)
    for q in range(num_qubits):
        op = np.kron(op, h if q == qubit else np.eye(2, dtype=complex))
    return op @ state


def _cphase_on_qubits(
    state: np.ndarray, control: int, target: int, angle: float, num_qubits: int
) -> np.ndarray:
    """Apply controlled-phase gate between control and target qubits."""
    n = 2**num_qubits
    new_state = state.copy()
    for i in range(n):
        bits = format(i, f"0{num_qubits}b")
        if bits[control] == "1" and bits[target] == "1":
            new_state[i] *= np.exp(1j * angle)
    return new_state


def _swap_qubits(
    state: np.ndarray, q1: int, q2: int, num_qubits: int
) -> np.ndarray:
    """Swap two qubits in the state vector."""
    n = 2**num_qubits
    new_state = np.zeros(n, dtype=complex)
    for i in range(n):
        bits = list(format(i, f"0{num_qubits}b"))
        bits[q1], bits[q2] = bits[q2], bits[q1]
        j = int("".join(bits), 2)
        new_state[j] = state[i]
    return new_state


def gate_sequence_qft(state: np.ndarray) -> np.ndarray:
    """
    QFT by simulating the actual quantum circuit gate-by-gate:
      For each qubit q (from MSB to LSB):
        1. Apply Hadamard to q
        2. Apply controlled-phase R_k from each subsequent qubit

      Then swap qubits to reverse bit order.

    This is the most faithful simulation of real quantum hardware.

    >>> s = np.array([1, 0, 0, 0], dtype=complex)
    >>> r = gate_sequence_qft(s)
    >>> np.allclose(np.abs(r)**2, [0.25, 0.25, 0.25, 0.25])
    True

    >>> s2 = np.array([1, 0], dtype=complex)
    >>> r2 = gate_sequence_qft(s2)
    >>> np.allclose(r2, [1/np.sqrt(2), 1/np.sqrt(2)])
    True
    """
    state = np.asarray(state, dtype=complex)
    n = len(state)
    num_qubits = int(np.log2(n))

    for i in range(num_qubits):
        state = _hadamard_on_qubit(state, i, num_qubits)
        for j in range(i + 1, num_qubits):
            angle = np.pi / (2 ** (j - i))
            state = _cphase_on_qubits(state, j, i, angle, num_qubits)

    # Reverse qubit order (swap first with last, etc.)
    for k in range(num_qubits // 2):
        state = _swap_qubits(state, k, num_qubits - k - 1, num_qubits)

    return state


# ---------------------------------------------------------------------------
# Correctness cross-check
# ---------------------------------------------------------------------------

def verify_all_variants(num_qubits: int = 3) -> bool:
    """
    Verify that all four variants produce identical results.

    >>> verify_all_variants(2)
    True
    >>> verify_all_variants(3)
    True
    """
    n = 2**num_qubits
    rng = np.random.default_rng(42)
    state = rng.random(n) + 1j * rng.random(n)
    state /= np.linalg.norm(state)  # normalise

    results = {
        "naive_recursive": naive_qft_recursive(state),
        "matrix_qft": matrix_qft(state),
        "classical_fft": classical_fft(state),
        "gate_sequence": gate_sequence_qft(state),
    }

    reference = results["matrix_qft"]
    return all(np.allclose(v, reference) for v in results.values())


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark(qubit_range: range | None = None, runs: int = 5) -> None:
    """
    Benchmark all QFT variants across different qubit counts.

    Prints a comparison table with average execution times.
    """
    if qubit_range is None:
        qubit_range = range(2, 9)

    variants: list[tuple[str, Callable]] = [
        ("naive_recursive", naive_qft_recursive),
        ("matrix_qft", matrix_qft),
        ("classical_fft", classical_fft),
        ("gate_sequence", gate_sequence_qft),
    ]

    header = f"{'Qubits':>6} {'N':>6}"
    for name, _ in variants:
        header += f" {name:>18}"
    print(header)
    print("-" * len(header))

    for q in qubit_range:
        n = 2**q
        rng = np.random.default_rng(0)
        state = rng.random(n) + 1j * rng.random(n)
        state /= np.linalg.norm(state)

        row = f"{q:>6} {n:>6}"
        for name, func in variants:
            # Skip gate_sequence for large sizes (too slow)
            if name == "gate_sequence" and q > 6:
                row += f" {'(skipped)':>18}"
                continue
            times = []
            for _ in range(runs):
                t0 = time.perf_counter()
                func(state)
                times.append(time.perf_counter() - t0)
            avg = sum(times) / len(times)
            if avg < 1e-3:
                row += f" {avg*1e6:>14.1f} us"
            elif avg < 1:
                row += f" {avg*1e3:>14.2f} ms"
            else:
                row += f" {avg:>14.3f}  s"
            row = row  # keep alignment
        print(row)


if __name__ == "__main__":
    print("=== QFT Variant Comparison ===\n")

    # Correctness check
    for q in (1, 2, 3, 4):
        ok = verify_all_variants(q)
        print(f"  {q}-qubit cross-check: {'PASS' if ok else 'FAIL'}")
    print()

    # Benchmark
    print("=== Benchmark (avg of 5 runs) ===\n")
    benchmark()
