"""
Polybius Square Cipher — Optimized Variants & Benchmark
=========================================================
Pure-Python implementations without NumPy dependency.
"""

import timeit

SQUARE_FLAT = [
    "a", "b", "c", "d", "e",
    "f", "g", "h", "i", "k",
    "l", "m", "n", "o", "p",
    "q", "r", "s", "t", "u",
    "v", "w", "x", "y", "z",
]

# Precompute lookup: char -> "rowcol" (both 1-based)
CHAR_TO_CODE: dict[str, str] = {
    SQUARE_FLAT[i]: str(i // 5 + 1) + str(i % 5 + 1) for i in range(25)
}
CODE_TO_CHAR: dict[str, str] = {v: k for k, v in CHAR_TO_CODE.items()}


# Variant 1: Dict lookup (replaces NumPy)
def encode_v1(message: str) -> str:
    message = message.lower().replace("j", "i")
    result = ""
    for c in message:
        if c == " ":
            result += " "
        elif c in CHAR_TO_CODE:
            result += CHAR_TO_CODE[c]
    return result


# Variant 2: List comprehension
def encode_v2(message: str) -> str:
    message = message.lower().replace("j", "i")
    return "".join(
        CHAR_TO_CODE[c] if c != " " else " " for c in message if c in CHAR_TO_CODE or c == " "
    )


# Variant 3: Ordinal math (no dict needed for standard Latin letters)
_SKIP_J = "abcdefghiklmnopqrstuvwxyz"  # 25 chars, no j


def encode_v3(message: str) -> str:
    message = message.lower().replace("j", "i")
    result: list[str] = []
    for c in message:
        if c == " ":
            result.append(" ")
        elif c in _SKIP_J:
            idx = _SKIP_J.index(c)
            result.append(str(idx // 5 + 1) + str(idx % 5 + 1))
    return "".join(result)


def decode_v1(code: str) -> str:
    code = code.replace(" ", "  ")
    result = ""
    for i in range(len(code) // 2):
        pair = code[i * 2 : i * 2 + 2]
        if pair[0] == " ":
            result += " "
        else:
            result += CODE_TO_CHAR.get(pair, "?")
    return result


def benchmark(n: int = 100_000) -> None:
    setup = (
        "from __main__ import encode_v1, encode_v2, encode_v3; "
        "msg = 'test message'"
    )
    t1 = timeit.timeit("encode_v1(msg)", setup=setup, number=n)
    t2 = timeit.timeit("encode_v2(msg)", setup=setup, number=n)
    t3 = timeit.timeit("encode_v3(msg)", setup=setup, number=n)
    print(f"V1 (dict lookup): {t1:.4f}s for {n:,} runs")
    print(f"V2 (listcomp)   : {t2:.4f}s for {n:,} runs")
    print(f"V3 (ord math)   : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "test message"
    enc = encode_v1(msg)
    print("V1 encoded:", enc)
    print("V2 encoded:", encode_v2(msg))
    print("V3 encoded:", encode_v3(msg))
    print("Decoded   :", decode_v1(enc))
    benchmark()
