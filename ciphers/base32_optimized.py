"""
Base32 Encoding — Optimized Variants + Benchmark

Compares manual binary approach, format-string approach, and stdlib base64.
"""

import base64
from timeit import timeit

B32_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"


# ── Variant 1: manual binary string (original) ───────────────────────────────
def base32_encode_v1(data: bytes) -> bytes:
    binary_data = "".join(bin(ord(d))[2:].zfill(8) for d in data.decode("utf-8"))
    binary_data = binary_data.ljust(5 * ((len(binary_data) // 5) + 1), "0")
    b32_chunks = map("".join, zip(*[iter(binary_data)] * 5))
    b32_result = "".join(B32_CHARSET[int(chunk, 2)] for chunk in b32_chunks)
    return bytes(b32_result.ljust(8 * ((len(b32_result) // 8) + 1), "="), "utf-8")


# ── Variant 2: integer shift approach ────────────────────────────────────────
def base32_encode_v2(data: bytes) -> bytes:
    """Process bytes directly using integer bit manipulation."""
    bits = 0
    bit_count = 0
    output = []
    for byte in data:
        bits = (bits << 8) | byte
        bit_count += 8
        while bit_count >= 5:
            bit_count -= 5
            output.append(B32_CHARSET[(bits >> bit_count) & 0x1F])
    if bit_count > 0:
        output.append(B32_CHARSET[(bits << (5 - bit_count)) & 0x1F])
    # Pad to multiple of 8
    while len(output) % 8 != 0:
        output.append("=")
    return "".join(output).encode()


# ── Variant 3: stdlib base64 ──────────────────────────────────────────────────
def base32_encode_v3(data: bytes) -> bytes:
    return base64.b32encode(data)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    data = b"Hello World! This is a base32 benchmark test string." * 3
    n = 50_000

    setup = (
        f"from __main__ import base32_encode_v1, base32_encode_v2, base32_encode_v3; "
        f"d={data!r}"
    )
    print("=== Base32 Benchmark (50k iterations) ===")
    for name, stmt in [
        ("encode_v1 (binary string)", "base32_encode_v1(d)"),
        ("encode_v2 (bit manipulation)", "base32_encode_v2(d)"),
        ("encode_v3 (stdlib b32encode)", "base32_encode_v3(d)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
