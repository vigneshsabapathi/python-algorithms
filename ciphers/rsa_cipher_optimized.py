"""
RSA Cipher — Optimized Variants & Benchmark
=============================================
Three approaches to RSA block encoding/decryption.
"""

import timeit

BYTE_SIZE = 256


# Variant 1: Original byte-by-byte accumulation (little-endian)
def get_blocks_v1(message: str, block_size: int = 128) -> list[int]:
    msg_bytes = message.encode("ascii")
    blocks = []
    for bs in range(0, len(msg_bytes), block_size):
        block_int = 0
        for i in range(bs, min(bs + block_size, len(msg_bytes))):
            block_int += msg_bytes[i] * (BYTE_SIZE ** (i % block_size))
        blocks.append(block_int)
    return blocks


# Variant 2: int.from_bytes (built-in, hardware-accelerated)
def get_blocks_v2(message: str, block_size: int = 128) -> list[int]:
    msg_bytes = message.encode("ascii")
    return [
        int.from_bytes(msg_bytes[i : i + block_size], byteorder="little")
        for i in range(0, len(msg_bytes), block_size)
    ]


# Variant 3: Power-of-256 via base conversion
def get_blocks_v3(message: str, block_size: int = 128) -> list[int]:
    msg_bytes = message.encode("ascii")
    blocks = []
    for i in range(0, len(msg_bytes), block_size):
        chunk = msg_bytes[i : i + block_size]
        n = 0
        for b in reversed(chunk):
            n = n * 256 + b
        blocks.append(n)
    return blocks


def encrypt(message: str, n: int, e: int, block_size: int = 1) -> list[int]:
    return [pow(b, e, n) for b in get_blocks_v1(message, block_size)]


def decrypt_to_text(blocks: list[int], msg_len: int, n: int, d: int, block_size: int = 1) -> str:
    dec = [pow(b, d, n) for b in blocks]
    msg: list[str] = []
    for bi in dec:
        part: list[str] = []
        for i in range(block_size - 1, -1, -1):
            if len(msg) + i < msg_len:
                ascii_num = bi // (256**i)
                bi %= 256**i
                part.insert(0, chr(ascii_num))
        msg.extend(part)
    return "".join(msg)


def benchmark(n_iters: int = 10_000) -> None:
    setup = (
        "from __main__ import get_blocks_v1, get_blocks_v2, get_blocks_v3; "
        "msg = 'Hello World, this is RSA!' * 3"
    )
    t1 = timeit.timeit("get_blocks_v1(msg, 8)", setup=setup, number=n_iters)
    t2 = timeit.timeit("get_blocks_v2(msg, 8)", setup=setup, number=n_iters)
    t3 = timeit.timeit("get_blocks_v3(msg, 8)", setup=setup, number=n_iters)
    print(f"V1 (manual accum)  : {t1:.4f}s for {n_iters:,} runs")
    print(f"V2 (int.from_bytes): {t2:.4f}s for {n_iters:,} runs")
    print(f"V3 (base-256 rev)  : {t3:.4f}s for {n_iters:,} runs")


if __name__ == "__main__":
    # p=17, q=19, n=323, e=5, d=173
    n, e, d = 323, 5, 173
    msg = "Hi"
    enc = encrypt(msg, n, e, block_size=1)
    dec = decrypt_to_text(enc, len(msg), n, d, block_size=1)
    print(f"Original : {msg}")
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")
    benchmark()
