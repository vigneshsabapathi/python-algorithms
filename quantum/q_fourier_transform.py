"""
Quantum Fourier Transform (QFT) — pure NumPy simulation.

The QFT maps an n-qubit quantum state |x> to a superposition of all
basis states with phases determined by x.  It is the quantum analogue
of the discrete Fourier transform and a key building block for
Shor's algorithm, quantum phase estimation, and quantum arithmetic.

For an n-qubit register the QFT unitary is the DFT matrix scaled by
1/sqrt(N) where N = 2^n:

    QFT|j> = (1/sqrt(N)) * sum_{k=0}^{N-1} omega^{jk} |k>
    omega  = e^{2*pi*i / N}

References:
    https://en.wikipedia.org/wiki/Quantum_Fourier_transform
    Nielsen & Chuang, "Quantum Computation and Quantum Information", Ch. 5

Adapted from TheAlgorithms/Python (original used Qiskit).
Rewritten as a dependency-free NumPy simulation for clarity.
"""

from __future__ import annotations

import numpy as np


def build_qft_matrix(num_qubits: int) -> np.ndarray:
    """
    Build the N x N QFT unitary matrix for *num_qubits* qubits.

    N = 2^num_qubits.  Entry (j, k) = omega^{jk} / sqrt(N).

    Args:
        num_qubits: positive integer, number of qubits (1..10).

    Returns:
        Complex ndarray of shape (N, N).

    >>> build_qft_matrix(1).shape
    (2, 2)
    >>> m = build_qft_matrix(2)
    >>> m.shape
    (4, 4)
    >>> np.allclose(m @ m.conj().T, np.eye(4))
    True
    >>> build_qft_matrix(0)
    Traceback (most recent call last):
        ...
    ValueError: num_qubits must be a positive integer, got 0.
    >>> build_qft_matrix(-3)
    Traceback (most recent call last):
        ...
    ValueError: num_qubits must be a positive integer, got -3.
    >>> build_qft_matrix('a')
    Traceback (most recent call last):
        ...
    TypeError: num_qubits must be an integer, got str.
    >>> build_qft_matrix(3.5)
    Traceback (most recent call last):
        ...
    TypeError: num_qubits must be an integer, got float.
    >>> build_qft_matrix(11)
    Traceback (most recent call last):
        ...
    ValueError: num_qubits too large to simulate (max 10), got 11.
    """
    if not isinstance(num_qubits, int):
        raise TypeError(
            f"num_qubits must be an integer, got {type(num_qubits).__name__}."
        )
    if num_qubits <= 0:
        raise ValueError(
            f"num_qubits must be a positive integer, got {num_qubits}."
        )
    if num_qubits > 10:
        raise ValueError(
            f"num_qubits too large to simulate (max 10), got {num_qubits}."
        )

    n = 2**num_qubits
    omega = np.exp(2j * np.pi / n)
    indices = np.arange(n)
    # outer product j*k gives exponent matrix
    return omega ** np.outer(indices, indices) / np.sqrt(n)


def apply_qft(state: np.ndarray, num_qubits: int | None = None) -> np.ndarray:
    """
    Apply the Quantum Fourier Transform to a state vector.

    Args:
        state:      1-D complex array of length N = 2^num_qubits.
        num_qubits: inferred from len(state) if omitted.

    Returns:
        Transformed state vector (complex ndarray of same length).

    >>> s = np.array([1, 0, 0, 0], dtype=complex)
    >>> result = apply_qft(s)
    >>> np.allclose(result, [0.5, 0.5, 0.5, 0.5])
    True

    >>> s2 = np.array([1, 0], dtype=complex)
    >>> result2 = apply_qft(s2)
    >>> np.allclose(result2, [1/np.sqrt(2), 1/np.sqrt(2)])
    True

    >>> apply_qft(np.array([1, 0, 0], dtype=complex))
    Traceback (most recent call last):
        ...
    ValueError: state length must be a power of 2, got 3.
    """
    state = np.asarray(state, dtype=complex)
    n = len(state)
    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError(f"state length must be a power of 2, got {n}.")
    if num_qubits is None:
        num_qubits = int(np.log2(n))
    qft_mat = build_qft_matrix(num_qubits)
    return qft_mat @ state


def inverse_qft(state: np.ndarray, num_qubits: int | None = None) -> np.ndarray:
    """
    Apply the inverse QFT (QFT-dagger) to a state vector.

    >>> s = np.array([1, 0, 0, 0], dtype=complex)
    >>> roundtrip = inverse_qft(apply_qft(s))
    >>> np.allclose(roundtrip, s)
    True
    """
    state = np.asarray(state, dtype=complex)
    n = len(state)
    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError(f"state length must be a power of 2, got {n}.")
    if num_qubits is None:
        num_qubits = int(np.log2(n))
    qft_mat = build_qft_matrix(num_qubits)
    return qft_mat.conj().T @ state


def measure_probabilities(state: np.ndarray) -> dict[str, float]:
    """
    Convert a state vector to measurement probabilities (Born rule).

    Returns a dict mapping bitstring labels to probabilities.

    >>> probs = measure_probabilities(np.array([1, 0, 0, 0], dtype=complex))
    >>> probs
    {'00': 1.0, '01': 0.0, '10': 0.0, '11': 0.0}

    >>> probs2 = measure_probabilities(apply_qft(np.array([1,0,0,0], dtype=complex)))
    >>> all(abs(v - 0.25) < 1e-10 for v in probs2.values())
    True
    """
    state = np.asarray(state, dtype=complex)
    n = len(state)
    num_bits = int(np.log2(n))
    probabilities = np.abs(state) ** 2
    return {format(i, f"0{num_bits}b"): round(float(p), 10) for i, p in enumerate(probabilities)}


if __name__ == "__main__":
    print("=== Quantum Fourier Transform (pure NumPy simulation) ===\n")

    for qubits in (1, 2, 3):
        n = 2**qubits
        basis_0 = np.zeros(n, dtype=complex)
        basis_0[0] = 1.0

        transformed = apply_qft(basis_0, qubits)
        probs = measure_probabilities(transformed)

        print(f"--- {qubits}-qubit QFT on |{'0'*qubits}> ---")
        print(f"  State after QFT:  {np.round(transformed, 4)}")
        print(f"  Probabilities:    {probs}")

        # round-trip check
        recovered = inverse_qft(transformed, qubits)
        print(f"  Round-trip check: {np.allclose(recovered, basis_0)}")
        print()

    # QFT on a non-trivial state: |1> in 2-qubit system
    state_1 = np.array([0, 1, 0, 0], dtype=complex)
    print("--- 2-qubit QFT on |01> ---")
    result = apply_qft(state_1)
    print(f"  State after QFT:  {np.round(result, 4)}")
    print(f"  Probabilities:    {measure_probabilities(result)}")
    print()

    # Unitarity verification
    qft3 = build_qft_matrix(3)
    print(f"--- Unitarity check (3-qubit QFT) ---")
    print(f"  QFT @ QFT_dag = I? {np.allclose(qft3 @ qft3.conj().T, np.eye(8))}")
