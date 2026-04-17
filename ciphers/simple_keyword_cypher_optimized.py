"""
Simple Keyword Cipher — Optimized Variants & Benchmark
========================================================
"""

import timeit

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _build_map(key: str) -> dict[str, str]:
    """Build the substitution map from keyword."""
    key = "".join(dict.fromkeys(c for c in key.upper() if c.isalpha()))
    offset = len(key)
    cipher_map: dict[str, str] = {ALPHA[i]: c for i, c in enumerate(key)}
    for i in range(len(cipher_map), 26):
        char = ALPHA[i - offset]
        while char in key:
            offset -= 1
            char = ALPHA[i - offset]
        cipher_map[ALPHA[i]] = char
    return cipher_map


# Variant 1: Dict get per character
def encipher_v1(message: str, key: str) -> str:
    cipher_map = _build_map(key)
    return "".join(cipher_map.get(c, c) for c in message.upper())


# Variant 2: str.maketrans/translate
def encipher_v2(message: str, key: str) -> str:
    cipher_map = _build_map(key)
    table = str.maketrans(cipher_map)
    return message.upper().translate(table)


# Variant 3: Prebuilt string indexing
def encipher_v3(message: str, key: str) -> str:
    cipher_map = _build_map(key)
    cipher_str = "".join(cipher_map.get(ALPHA[i], ALPHA[i]) for i in range(26))
    return "".join(
        cipher_str[ord(c) - 65] if "A" <= c <= "Z" else c
        for c in message.upper()
    )


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encipher_v1, encipher_v2, encipher_v3; "
        "key = 'Goodbye!!'; msg = 'Hello World!'"
    )
    t1 = timeit.timeit("encipher_v1(msg, key)", setup=setup, number=n)
    t2 = timeit.timeit("encipher_v2(msg, key)", setup=setup, number=n)
    t3 = timeit.timeit("encipher_v3(msg, key)", setup=setup, number=n)
    print(f"V1 (dict.get)    : {t1:.4f}s for {n:,} runs")
    print(f"V2 (maketrans)   : {t2:.4f}s for {n:,} runs")
    print(f"V3 (str index)   : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    key = "Goodbye!!"
    msg = "Hello World!!"
    print("V1:", encipher_v1(msg, key))
    print("V2:", encipher_v2(msg, key))
    print("V3:", encipher_v3(msg, key))
    benchmark()
