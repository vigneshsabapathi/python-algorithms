"""
Fractionated Morse Cipher — Optimized Variants + Benchmark

Three encryption strategies: original generator, list-based, precomputed table.
"""

import string
from timeit import timeit

MORSE_CODE_DICT: dict[str, str] = {
    "A": ".-",   "B": "-...", "C": "-.-.", "D": "-..",  "E": ".",
    "F": "..-.", "G": "--.",  "H": "....", "I": "..",   "J": ".---",
    "K": "-.-",  "L": ".-..", "M": "--",   "N": "-.",   "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",  "S": "...",  "T": "-",
    "U": "..-",  "V": "...-", "W": ".--",  "X": "-..-", "Y": "-.--",
    "Z": "--..",  " ": "",
}

MORSE_COMBINATIONS: list[str] = [
    "...", "..-", "..x", ".-.", ".--", ".-x", ".x.", ".x-", ".xx",
    "-..", "-.-", "-.x", "--.", "---", "--x", "-x.", "-x-", "-xx",
    "x..", "x.-", "x.x", "x-.", "x--", "x-x", "xx.", "xx-", "xxx",
]

REVERSE_MORSE: dict[str, str] = {v: k for k, v in MORSE_CODE_DICT.items()}


def _build_key_alphabet(key: str) -> str:
    k = key.upper() + string.ascii_uppercase
    return "".join(sorted(set(k), key=k.find))


def _to_morse(plaintext: str) -> str:
    return "x".join(MORSE_CODE_DICT.get(ch.upper(), "") for ch in plaintext)


# ── Variant 1: original generator join ───────────────────────────────────────
def encrypt_v1(plaintext: str, key: str) -> str:
    morse = _to_morse(plaintext)
    key_alpha = _build_key_alphabet(key)
    padding = (-len(morse)) % 3
    morse += "x" * padding
    t_map = {v: k for k, v in zip(key_alpha, MORSE_COMBINATIONS)}
    t_map["xxx"] = ""
    return "".join(t_map[morse[i:i+3]] for i in range(0, len(morse), 3))


# ── Variant 2: list accumulation ─────────────────────────────────────────────
def encrypt_v2(plaintext: str, key: str) -> str:
    morse = _to_morse(plaintext)
    key_alpha = _build_key_alphabet(key)
    padding = (-len(morse)) % 3
    morse += "x" * padding
    t_map = {v: k for k, v in zip(key_alpha, MORSE_COMBINATIONS)}
    t_map["xxx"] = ""
    result = []
    for i in range(0, len(morse), 3):
        result.append(t_map[morse[i:i+3]])
    return "".join(result)


# ── Variant 3: precompute and reuse trigram map ───────────────────────────────
def _build_encrypt_map(key: str) -> dict[str, str]:
    key_alpha = _build_key_alphabet(key)
    t_map = {v: k for k, v in zip(key_alpha, MORSE_COMBINATIONS)}
    t_map["xxx"] = ""
    return t_map


def encrypt_v3(plaintext: str, t_map: dict[str, str]) -> str:
    """Precomputed map variant (best when encrypting many messages with same key)."""
    morse = _to_morse(plaintext)
    padding = (-len(morse)) % 3
    morse += "x" * padding
    return "".join(t_map[morse[i:i+3]] for i in range(0, len(morse), 3))


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    plaintext = "defend the east wall" * 3
    key = "ROUNDTABLE"
    t_map = _build_encrypt_map(key)
    n = 20_000

    setup = (
        f"from __main__ import encrypt_v1, encrypt_v2, encrypt_v3, _build_encrypt_map; "
        f"pt={plaintext!r}; k={key!r}; "
        f"tm=_build_encrypt_map(k)"
    )
    print("=== Fractionated Morse Benchmark (20k iterations) ===")
    for name, stmt in [
        ("encrypt_v1 (generator)", "encrypt_v1(pt, k)"),
        ("encrypt_v2 (list)", "encrypt_v2(pt, k)"),
        ("encrypt_v3 (precomputed map)", "encrypt_v3(pt, tm)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
