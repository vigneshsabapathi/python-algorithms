"""
Morse Code — Optimized Variants & Benchmark
============================================
Three encoding/decoding approaches compared.
"""

import timeit

# fmt: off
MORSE_CODE_DICT = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.",
    "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.",
    "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-", "U": "..-",
    "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..", "1": ".----",
    "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.", "0": "-----", " ": "/",
}
# fmt: on
REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}


# Variant 1: join with list comprehension
def encrypt_v1(message: str) -> str:
    return " ".join(MORSE_CODE_DICT[c] for c in message.upper())


# Variant 2: manual loop with list append
def encrypt_v2(message: str) -> str:
    parts: list[str] = []
    for c in message.upper():
        parts.append(MORSE_CODE_DICT[c])
    return " ".join(parts)


# Variant 3: map + join
def encrypt_v3(message: str) -> str:
    return " ".join(map(MORSE_CODE_DICT.__getitem__, message.upper()))


def decrypt_v1(code: str) -> str:
    return "".join(REVERSE_DICT[tok] for tok in code.split())


def decrypt_v2(code: str) -> str:
    return "".join(map(REVERSE_DICT.__getitem__, code.split()))


def benchmark(n: int = 200_000) -> None:
    setup = "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; msg='HELLO WORLD'"
    t1 = timeit.timeit("encrypt_v1(msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(msg)", setup=setup, number=n)
    print(f"V1 (genexpr)  : {t1:.4f}s for {n:,} runs")
    print(f"V2 (append)   : {t2:.4f}s for {n:,} runs")
    print(f"V3 (map)      : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "HELLO WORLD"
    enc = encrypt_v1(msg)
    print("Encoded:", enc)
    print("Decoded:", decrypt_v1(enc))
    print()
    benchmark()
