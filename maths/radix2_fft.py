"""
Radix-2 Fast Fourier Transform
==============================
Iterative Cooley-Tukey FFT; input length must be a power of 2.
"""
import cmath
from typing import List


def fft(x: List[complex]) -> List[complex]:
    """
    >>> fft([1, 1, 1, 1])
    [(4+0j), 0j, 0j, 0j]
    >>> r = fft([1, 0, 0, 0])
    >>> all(abs(z - 1) < 1e-9 for z in r)
    True
    """
    n = len(x)
    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError("length must be a power of 2")
    a = [complex(v) for v in x]
    # bit-reversal permutation
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    # butterfly
    size = 2
    while size <= n:
        half = size // 2
        w0 = cmath.exp(-2j * cmath.pi / size)
        for start in range(0, n, size):
            w = 1 + 0j
            for k in range(half):
                t = w * a[start + k + half]
                a[start + k + half] = a[start + k] - t
                a[start + k] = a[start + k] + t
                w *= w0
        size <<= 1
    return a


def ifft(X: List[complex]) -> List[complex]:
    """
    >>> a = [1, 2, 3, 4]
    >>> r = ifft(fft(a))
    >>> all(abs(z.real - b) < 1e-9 for z, b in zip(r, a))
    True
    """
    n = len(X)
    conj = [v.conjugate() for v in X]
    y = fft(conj)
    return [v.conjugate() / n for v in y]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    x = [1, 2, 3, 4]
    X = fft(x)
    print("FFT:", [f"{v.real:.3f}+{v.imag:.3f}j" for v in X])
    print("IFFT:", [f"{v.real:.3f}" for v in ifft(X)])
