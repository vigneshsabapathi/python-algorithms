"""
Mel-Frequency Cepstral Coefficients (MFCC)

Audio feature extraction technique widely used in speech recognition.
Converts audio signal to compact representation based on human
auditory perception.

Steps: Pre-emphasis -> Framing -> Windowing -> FFT -> Mel filterbank -> Log -> DCT

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/mfcc.py
"""

import numpy as np


def hz_to_mel(hz: float) -> float:
    """
    Convert frequency in Hz to Mel scale.

    >>> round(hz_to_mel(1000), 0)
    1000.0
    >>> round(hz_to_mel(0), 2)
    0.0
    """
    return 2595 * np.log10(1 + hz / 700)


def mel_to_hz(mel: float) -> float:
    """
    Convert Mel scale to frequency in Hz.

    >>> round(mel_to_hz(1000), 0)
    1000.0
    >>> round(mel_to_hz(0), 2)
    0.0
    """
    return 700 * (10 ** (mel / 2595) - 1)


def pre_emphasis(signal: np.ndarray, alpha: float = 0.97) -> np.ndarray:
    """
    Apply pre-emphasis filter to boost high frequencies.

    y[t] = x[t] - alpha * x[t-1]

    >>> pre_emphasis(np.array([1.0, 2.0, 3.0, 4.0]), 0.97)
    array([1.  , 1.03, 1.06, 1.09])
    """
    return np.append(signal[0], signal[1:] - alpha * signal[:-1])


def frame_signal(
    signal: np.ndarray,
    frame_length: int,
    frame_step: int,
) -> np.ndarray:
    """
    Split signal into overlapping frames.

    >>> frames = frame_signal(np.arange(10, dtype=float), 4, 2)
    >>> frames.shape[1]
    4
    >>> frames[0, 0]
    0.0
    """
    signal_length = len(signal)
    n_frames = 1 + (signal_length - frame_length) // frame_step

    indices = (
        np.arange(frame_length)[np.newaxis, :]
        + np.arange(n_frames)[:, np.newaxis] * frame_step
    )
    return signal[indices]


def create_mel_filterbank(
    n_filters: int,
    n_fft: int,
    sample_rate: int,
    low_freq: float = 0,
    high_freq: float | None = None,
) -> np.ndarray:
    """
    Create Mel-spaced triangular filterbank.

    >>> fb = create_mel_filterbank(10, 256, 8000)
    >>> fb.shape
    (10, 129)
    """
    high_freq = high_freq or sample_rate / 2

    low_mel = hz_to_mel(low_freq)
    high_mel = hz_to_mel(high_freq)

    # Equally spaced mel points
    mel_points = np.linspace(low_mel, high_mel, n_filters + 2)
    hz_points = np.array([mel_to_hz(m) for m in mel_points])

    # Convert to FFT bin numbers
    bins = np.floor((n_fft + 1) * hz_points / sample_rate).astype(int)

    filterbank = np.zeros((n_filters, n_fft // 2 + 1))

    for i in range(n_filters):
        for j in range(int(bins[i]), int(bins[i + 1])):
            filterbank[i, j] = (j - bins[i]) / (bins[i + 1] - bins[i] + 1e-15)
        for j in range(int(bins[i + 1]), int(bins[i + 2])):
            filterbank[i, j] = (bins[i + 2] - j) / (bins[i + 2] - bins[i + 1] + 1e-15)

    return filterbank


def compute_mfcc(
    signal: np.ndarray,
    sample_rate: int = 16000,
    n_mfcc: int = 13,
    n_filters: int = 26,
    n_fft: int = 512,
    frame_length: int = 400,
    frame_step: int = 160,
    pre_emph: float = 0.97,
) -> np.ndarray:
    """
    Compute MFCC features from audio signal.

    >>> np.random.seed(42)
    >>> signal = np.random.randn(16000)  # 1 second of audio at 16kHz
    >>> mfcc = compute_mfcc(signal, sample_rate=16000, n_mfcc=13)
    >>> mfcc.shape[1]
    13
    """
    # 1. Pre-emphasis
    emphasized = pre_emphasis(signal, pre_emph)

    # 2. Framing
    frames = frame_signal(emphasized, frame_length, frame_step)

    # 3. Windowing (Hamming)
    window = np.hamming(frame_length)
    windowed = frames * window

    # 4. FFT
    mag_spectrum = np.abs(np.fft.rfft(windowed, n_fft))
    power_spectrum = mag_spectrum**2 / n_fft

    # 5. Mel filterbank
    filterbank = create_mel_filterbank(n_filters, n_fft, sample_rate)
    mel_spectrum = power_spectrum @ filterbank.T

    # 6. Log
    mel_spectrum = np.log(mel_spectrum + 1e-15)

    # 7. DCT (Type-II)
    n_frames = mel_spectrum.shape[0]
    mfcc = np.zeros((n_frames, n_mfcc))
    for k in range(n_mfcc):
        for n in range(n_filters):
            mfcc[:, k] += mel_spectrum[:, n] * np.cos(
                np.pi * k * (2 * n + 1) / (2 * n_filters)
            )

    return mfcc


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- MFCC Demo ---")
    np.random.seed(42)

    # Simulate audio signal (1 second at 16kHz)
    sample_rate = 16000
    duration = 1.0
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.3 * np.sin(2 * np.pi * 880 * t)
    signal += np.random.randn(len(signal)) * 0.01

    mfcc = compute_mfcc(signal, sample_rate=sample_rate, n_mfcc=13)
    print(f"Signal length: {len(signal)} samples ({duration}s at {sample_rate}Hz)")
    print(f"MFCC shape: {mfcc.shape} (frames x coefficients)")
    print(f"MFCC[0] (first frame): {np.round(mfcc[0], 3)}")
    print(f"MFCC mean: {np.round(np.mean(mfcc, axis=0), 3)}")
    print(f"MFCC std:  {np.round(np.std(mfcc, axis=0), 3)}")
