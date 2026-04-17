"""
Chi-Squared Caesar Decrypt — Optimized Variants + Benchmark

Three scoring strategies: per-letter loop, Counter-based, numpy-based.
"""

from collections import Counter
from timeit import timeit

ENGLISH_FREQUENCIES: dict[str, float] = {
    "a": 0.08497, "b": 0.01492, "c": 0.02202, "d": 0.04253,
    "e": 0.11162, "f": 0.02228, "g": 0.02015, "h": 0.06094,
    "i": 0.07546, "j": 0.00153, "k": 0.01292, "l": 0.04025,
    "m": 0.02406, "n": 0.06749, "o": 0.07507, "p": 0.01929,
    "q": 0.00095, "r": 0.07587, "s": 0.06327, "t": 0.09356,
    "u": 0.02758, "v": 0.00978, "w": 0.02560, "x": 0.00150,
    "y": 0.01994, "z": 0.00077,
}
_ALPHABET = [chr(i) for i in range(97, 123)]


# ── Variant 1: original per-letter chi-squared ────────────────────────────────
def decrypt_v1(ciphertext: str) -> tuple[int, float, str]:
    ct = ciphertext.lower()
    best_key, best_chi, best_text = 0, float("inf"), ct
    for shift in range(26):
        dec = "".join(
            _ALPHABET[(ord(c) - 97 - shift) % 26] if c.islower() else c
            for c in ct
        )
        chi = sum(
            ((dec.count(ch) - ENGLISH_FREQUENCIES[ch] * dec.count(ch)) ** 2)
            / (ENGLISH_FREQUENCIES[ch] * dec.count(ch))
            for ch in ENGLISH_FREQUENCIES
            if dec.count(ch) > 0
        )
        if chi < best_chi:
            best_key, best_chi, best_text = shift, chi, dec
    return best_key, best_chi, best_text


# ── Variant 2: Counter-based (single pass per shift) ─────────────────────────
def decrypt_v2(ciphertext: str) -> tuple[int, float, str]:
    ct = ciphertext.lower()
    total = sum(1 for c in ct if c.isalpha())
    best_key, best_chi, best_text = 0, float("inf"), ct
    for shift in range(26):
        dec = "".join(
            _ALPHABET[(ord(c) - 97 - shift) % 26] if c.islower() else c
            for c in ct
        )
        counts = Counter(c for c in dec if c.isalpha())
        chi = 0.0
        for ch, freq in ENGLISH_FREQUENCIES.items():
            observed = counts.get(ch, 0)
            expected = freq * total
            if expected > 0:
                chi += (observed - expected) ** 2 / expected
        if chi < best_chi:
            best_key, best_chi, best_text = shift, chi, dec
    return best_key, best_chi, best_text


# ── Variant 3: numpy vectorized ───────────────────────────────────────────────
def decrypt_v3(ciphertext: str) -> tuple[int, float, str]:
    try:
        import numpy as np
    except ImportError:
        return decrypt_v2(ciphertext)

    ct = ciphertext.lower()
    letters_only = [c for c in ct if c.isalpha()]
    n = len(letters_only)
    letter_indices = np.array([ord(c) - 97 for c in letters_only])
    expected = np.array([ENGLISH_FREQUENCIES.get(chr(i + 97), 0) for i in range(26)]) * n
    alphabet_list = list(ENGLISH_FREQUENCIES.keys())

    best_key, best_chi, best_text = 0, float("inf"), ct
    for shift in range(26):
        shifted = (letter_indices - shift) % 26
        counts = np.bincount(shifted, minlength=26).astype(float)
        nonzero = expected > 0
        chi = float(np.sum(((counts[nonzero] - expected[nonzero]) ** 2) / expected[nonzero]))
        if chi < best_chi:
            best_chi = chi
            best_key = shift
            best_text = "".join(
                chr((ord(c) - 97 - shift) % 26 + 97) if c.isalpha() else c
                for c in ct
            )
    return best_key, best_chi, best_text


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    ct = "dof pz aol jhlzhy jpwoly zv wvwbshy? pa pz avv lhzf av jyhjr!"
    n = 500

    setup = (
        f"from __main__ import decrypt_v1, decrypt_v2, decrypt_v3; ct={ct!r}"
    )
    print("=== Chi-Squared Decrypt Benchmark (500 iterations) ===")
    for name, stmt in [
        ("decrypt_v1 (per-letter loop)", "decrypt_v1(ct)"),
        ("decrypt_v2 (Counter-based)", "decrypt_v2(ct)"),
        ("decrypt_v3 (numpy)", "decrypt_v3(ct)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
