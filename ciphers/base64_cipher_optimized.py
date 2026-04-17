"""
Base64 Encoding — Optimized Variants + Benchmark

Compares manual binary string, integer bit-shift, and stdlib base64.
"""

import base64
from timeit import timeit

B64_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


# ── Variant 1: manual binary string (original) ───────────────────────────────
def base64_encode_v1(data: bytes) -> bytes:
    binary_stream = "".join(bin(byte)[2:].zfill(8) for byte in data)
    padding_needed = len(binary_stream) % 6 != 0
    if padding_needed:
        padding = b"=" * ((6 - len(binary_stream) % 6) // 2)
        binary_stream += "0" * (6 - len(binary_stream) % 6)
    else:
        padding = b""
    return (
        "".join(
            B64_CHARSET[int(binary_stream[i : i + 6], 2)]
            for i in range(0, len(binary_stream), 6)
        ).encode()
        + padding
    )


# ── Variant 2: integer bit-shift (no binary strings) ─────────────────────────
def base64_encode_v2(data: bytes) -> bytes:
    """Process 3-byte groups as a 24-bit integer."""
    out = []
    # Pad data to multiple of 3
    pad = (-len(data)) % 3
    data_padded = data + b"\x00" * pad
    for i in range(0, len(data_padded), 3):
        n = (data_padded[i] << 16) | (data_padded[i + 1] << 8) | data_padded[i + 2]
        out.append(B64_CHARSET[(n >> 18) & 0x3F])
        out.append(B64_CHARSET[(n >> 12) & 0x3F])
        out.append(B64_CHARSET[(n >> 6) & 0x3F])
        out.append(B64_CHARSET[n & 0x3F])
    result = "".join(out)
    if pad:
        result = result[:-pad] + "=" * pad
    return result.encode()


# ── Variant 3: stdlib base64 (C implementation) ───────────────────────────────
def base64_encode_v3(data: bytes) -> bytes:
    return base64.b64encode(data)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    data = b"The quick brown fox jumps over the lazy dog. " * 5
    n = 50_000

    setup = (
        f"from __main__ import base64_encode_v1, base64_encode_v2, base64_encode_v3; "
        f"d={data!r}"
    )
    print("=== Base64 Benchmark (50k iterations) ===")
    for name, stmt in [
        ("encode_v1 (binary string)", "base64_encode_v1(d)"),
        ("encode_v2 (bit-shift 3-byte)", "base64_encode_v2(d)"),
        ("encode_v3 (stdlib b64encode)", "base64_encode_v3(d)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
