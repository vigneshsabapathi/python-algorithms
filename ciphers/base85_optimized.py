"""
Base85 (Ascii85) — Optimized Variants + Benchmark

Compares original recursive approach, iterative, and stdlib.
"""

import base64
from timeit import timeit


# ── Variant 1: original recursive helper ─────────────────────────────────────
def _b10_to_85_v1(d: int) -> str:
    return "".join(chr(d % 85 + 33)) + _b10_to_85_v1(d // 85) if d > 0 else ""


def ascii85_encode_v1(data: bytes) -> bytes:
    binary_data = "".join(bin(ord(d))[2:].zfill(8) for d in data.decode("utf-8"))
    null_values = (32 * ((len(binary_data) // 32) + 1) - len(binary_data)) // 8
    binary_data = binary_data.ljust(32 * ((len(binary_data) // 32) + 1), "0")
    b85_chunks = [int(_s, 2) for _s in map("".join, zip(*[iter(binary_data)] * 32))]
    result = "".join(_b10_to_85_v1(chunk)[::-1] for chunk in b85_chunks)
    return bytes(result[:-null_values] if null_values % 4 != 0 else result, "utf-8")


# ── Variant 2: iterative base-85 conversion ───────────────────────────────────
def _b10_to_85_v2(d: int) -> list[int]:
    digits = []
    for _ in range(5):
        digits.append(d % 85)
        d //= 85
    return digits[::-1]


def ascii85_encode_v2(data: bytes) -> bytes:
    pad = (-len(data)) % 4
    data_padded = data + b"\x00" * pad
    output = []
    for i in range(0, len(data_padded), 4):
        n = int.from_bytes(data_padded[i : i + 4], "big")
        output.extend(chr(d + 33) for d in _b10_to_85_v2(n))
    result = "".join(output)
    if pad:
        result = result[: -(pad)]
    return result.encode()


# ── Variant 3: stdlib base64.a85encode ────────────────────────────────────────
def ascii85_encode_v3(data: bytes) -> bytes:
    return base64.a85encode(data)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    data = b"Hello World benchmark for base 85 encoding!" * 3
    n = 20_000

    setup = (
        f"from __main__ import ascii85_encode_v1, ascii85_encode_v2, ascii85_encode_v3; "
        f"d={data!r}"
    )
    print("=== Base85 Benchmark (20k iterations) ===")
    for name, stmt in [
        ("encode_v1 (recursive)", "ascii85_encode_v1(d)"),
        ("encode_v2 (iterative)", "ascii85_encode_v2(d)"),
        ("encode_v3 (stdlib a85encode)", "ascii85_encode_v3(d)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
