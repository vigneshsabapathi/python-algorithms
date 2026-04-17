"""
Transposition Cipher File I/O — Optimized Variants & Benchmark
================================================================
Three approaches to in-memory transposition (file I/O itself is I/O-bound).
"""

import math
import timeit


# Variant 1: Original column-walking
def encrypt_v1(key: int, message: str) -> str:
    cols = [""] * key
    for col in range(key):
        ptr = col
        while ptr < len(message):
            cols[col] += message[ptr]
            ptr += key
    return "".join(cols)


# Variant 2: Stride slicing (Pythonic one-liner)
def encrypt_v2(key: int, message: str) -> str:
    return "".join(message[col::key] for col in range(key))


# Variant 3: Padded rectangular grid
def encrypt_v3(key: int, message: str) -> str:
    rows = math.ceil(len(message) / key)
    padded = message + "\x00" * (rows * key - len(message))
    return "".join(
        padded[col + row * key]
        for col in range(key)
        for row in range(rows)
        if col + row * key < len(message)
    )


def process_file_content(key: int, content: str, mode: str) -> str:
    """
    Process file *content* with columnar transposition.

    >>> process_file_content(6, 'Harshil Darji', 'encrypt')
    'Hlia rDsahrij'
    >>> process_file_content(6, 'Hlia rDsahrij', 'decrypt')
    'Harshil Darji'
    """
    if mode == "encrypt":
        return encrypt_v2(key, content)
    elif mode == "decrypt":
        num_cols = math.ceil(len(content) / key)
        num_rows = key
        num_shaded = (num_cols * num_rows) - len(content)
        plain = [""] * num_cols
        col = row = 0
        for sym in content:
            plain[col] += sym
            col += 1
            if col == num_cols or (col == num_cols - 1 and row >= num_rows - num_shaded):
                col = 0
                row += 1
        return "".join(plain)
    return content


def benchmark(n: int = 200_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "msg = 'Prehistoric men lived in caves and hunted mammoths.' * 10; key = 7"
    )
    t1 = timeit.timeit("encrypt_v1(key, msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(key, msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(key, msg)", setup=setup, number=n)
    print(f"V1 (walk)   : {t1:.4f}s for {n:,} runs")
    print(f"V2 (stride) : {t2:.4f}s for {n:,} runs")
    print(f"V3 (padded) : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    msg = "Prehistoric men lived in caves."
    key = 6
    enc = encrypt_v1(key, msg)
    print(f"V1: {enc}")
    enc2 = encrypt_v2(key, msg)
    print(f"V2: {enc2}")
    assert enc == enc2
    benchmark()
