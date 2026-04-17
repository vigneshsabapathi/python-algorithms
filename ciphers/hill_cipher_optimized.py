"""
Hill Cipher — Optimized Variants + Benchmark

Three encryption strategies: numpy matrix multiply (original), pure Python, scipy.
"""

import string
from math import gcd
from timeit import timeit

import numpy as np

KEY_STRING = string.ascii_uppercase + string.digits  # 36 chars
M = len(KEY_STRING)


def _check_key(key: np.ndarray) -> None:
    det = round(np.linalg.det(key)) % M
    if gcd(det, M) != 1:
        raise ValueError(f"Key determinant {det} is not coprime with {M}.")


def _process_text(text: str, block: int) -> str:
    chars = [c for c in text.upper() if c in KEY_STRING]
    while len(chars) % block != 0:
        chars.append(chars[-1])
    return "".join(chars)


# ── Variant 1: numpy per-block loop (original) ───────────────────────────────
def encrypt_v1(text: str, key: np.ndarray) -> str:
    _check_key(key)
    text = _process_text(text, key.shape[0])
    n = key.shape[0]
    encrypted = []
    for i in range(0, len(text), n):
        vec = np.array([[KEY_STRING.index(c)] for c in text[i:i+n]])
        result = (key.dot(vec) % M).T.tolist()[0]
        encrypted.extend(KEY_STRING[int(v)] for v in result)
    return "".join(encrypted)


# ── Variant 2: numpy bulk matrix (reshape all blocks at once) ────────────────
def encrypt_v2(text: str, key: np.ndarray) -> str:
    _check_key(key)
    text = _process_text(text, key.shape[0])
    n = key.shape[0]
    indices = np.array([KEY_STRING.index(c) for c in text]).reshape(-1, n).T
    encrypted_indices = (key.dot(indices) % M).T.flatten().astype(int)
    return "".join(KEY_STRING[i] for i in encrypted_indices)


# ── Variant 3: pure Python (no numpy) ────────────────────────────────────────
def _matmul_mod(a: list[list[int]], v: list[int], m: int) -> list[int]:
    n = len(a)
    return [sum(a[r][c] * v[c] for c in range(n)) % m for r in range(n)]


def encrypt_v3(text: str, key_list: list[list[int]]) -> str:
    n = len(key_list)
    chars = [c for c in text.upper() if c in KEY_STRING]
    while len(chars) % n != 0:
        chars.append(chars[-1])
    encrypted = []
    for i in range(0, len(chars), n):
        vec = [KEY_STRING.index(c) for c in chars[i:i+n]]
        result = _matmul_mod(key_list, vec, M)
        encrypted.extend(KEY_STRING[v] for v in result)
    return "".join(encrypted)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    key = np.array([[2, 5], [1, 6]])
    key_list = [[2, 5], [1, 6]]
    text = "hello world testing hill cipher benchmark" * 3
    n = 5_000

    setup = (
        f"import numpy as np; "
        f"from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        f"key=np.array([[2,5],[1,6]]); kl=[[2,5],[1,6]]; t={text!r}"
    )
    print("=== Hill Cipher Benchmark (5k iterations) ===")
    for name, stmt in [
        ("encrypt_v1 (numpy per-block)", "encrypt_v1(t, key)"),
        ("encrypt_v2 (numpy bulk)", "encrypt_v2(t, key)"),
        ("encrypt_v3 (pure Python)", "encrypt_v3(t, kl)"),
    ]:
        t_val = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t_val:.4f}s")


if __name__ == "__main__":
    benchmark()
