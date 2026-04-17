"""
Base16 (Hex) Encoding — Optimized Variants + Benchmark

Compares manual hex encoding against stdlib binascii and format string.
"""

from binascii import hexlify, unhexlify
from timeit import timeit


# ── Variant 1: manual hex (original) ─────────────────────────────────────────
def base16_encode_v1(data: bytes) -> str:
    return "".join(hex(b)[2:].zfill(2).upper() for b in data)


def base16_decode_v1(data: str) -> bytes:
    return bytes(int(data[i : i + 2], 16) for i in range(0, len(data), 2))


# ── Variant 2: format string ──────────────────────────────────────────────────
def base16_encode_v2(data: bytes) -> str:
    return "".join(f"{b:02X}" for b in data)


# ── Variant 3: stdlib binascii ───────────────────────────────────────────────
def base16_encode_v3(data: bytes) -> str:
    return hexlify(data).decode("ascii").upper()


def base16_decode_v3(data: str) -> bytes:
    return unhexlify(data)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    data = b"Hello World! This is a benchmark test." * 10
    encoded = base16_encode_v1(data)
    n = 100_000

    setup_enc = (
        f"from __main__ import base16_encode_v1, base16_encode_v2, base16_encode_v3; "
        f"d={data!r}"
    )
    setup_dec = (
        f"from __main__ import base16_decode_v1, base16_decode_v3; "
        f"e={encoded!r}"
    )

    print("=== Base16 Benchmark (100k iterations) ===")
    for name, stmt in [
        ("encode_v1 (hex + zfill)", "base16_encode_v1(d)"),
        ("encode_v2 (format :02X)", "base16_encode_v2(d)"),
        ("encode_v3 (binascii)", "base16_encode_v3(d)"),
    ]:
        t = timeit(stmt, setup=setup_enc, number=n)
        print(f"  {name}: {t:.4f}s")

    for name, stmt in [
        ("decode_v1 (int slice)", "base16_decode_v1(e)"),
        ("decode_v3 (unhexlify)", "base16_decode_v3(e)"),
    ]:
        t = timeit(stmt, setup=setup_dec, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
