"""
A1Z26 Cipher — Optimized Variants + Benchmark

Three implementation approaches for the A1Z26 encode/decode operation.
"""

from __future__ import annotations
from timeit import timeit


# ── Variant 1: list comprehension (original) ──────────────────────────────────
def encode_v1(plain: str) -> list[int]:
    """List comprehension using ord()."""
    return [ord(c) - 96 for c in plain]


def decode_v1(encoded: list[int]) -> str:
    """Generator join using chr()."""
    return "".join(chr(n + 96) for n in encoded)


# ── Variant 2: pre-built lookup dict ─────────────────────────────────────────
import string as _string

_ENCODE_MAP: dict[str, int] = {c: i for i, c in enumerate(_string.ascii_lowercase, 1)}
_DECODE_MAP: dict[int, str] = {i: c for i, c in enumerate(_string.ascii_lowercase, 1)}


def encode_v2(plain: str) -> list[int]:
    """Dict lookup — avoids ord() overhead for pure alpha strings."""
    return [_ENCODE_MAP[c] for c in plain]


def decode_v2(encoded: list[int]) -> str:
    """Dict lookup decode."""
    return "".join(_DECODE_MAP[n] for n in encoded)


# ── Variant 3: bytes arithmetic (fastest for ASCII) ──────────────────────────
def encode_v3(plain: str) -> list[int]:
    """Bytes-based: encode to ASCII bytes then subtract 96."""
    return [b - 96 for b in plain.encode("ascii")]


def decode_v3(encoded: list[int]) -> str:
    """Bytes-based decode."""
    return bytes(n + 96 for n in encoded).decode("ascii")


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    sample = "abcdefghijklmnopqrstuvwxyz" * 10
    encoded = encode_v1(sample)
    n = 100_000

    setup_enc = f"from __main__ import encode_v1, encode_v2, encode_v3; s='{sample}'"
    setup_dec = f"from __main__ import decode_v1, decode_v2, decode_v3; e={encoded}"

    print("=== A1Z26 Benchmark (100k iterations) ===")
    for name, stmt in [
        ("encode_v1 (ord)", f"encode_v1(s)"),
        ("encode_v2 (dict)", f"encode_v2(s)"),
        ("encode_v3 (bytes)", f"encode_v3(s)"),
    ]:
        t = timeit(stmt, setup=setup_enc, number=n)
        print(f"  {name}: {t:.4f}s")

    for name, stmt in [
        ("decode_v1 (chr join)", f"decode_v1(e)"),
        ("decode_v2 (dict)", f"decode_v2(e)"),
        ("decode_v3 (bytes)", f"decode_v3(e)"),
    ]:
        t = timeit(stmt, setup=setup_dec, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
