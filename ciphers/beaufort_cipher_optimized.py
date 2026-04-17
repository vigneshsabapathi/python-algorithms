"""
Beaufort Cipher — Optimized Variants + Benchmark

Three encryption strategies: dict lookup, ord() arithmetic, str.translate.
"""

import string
from timeit import timeit

_UPPER = string.ascii_uppercase
_DICT1 = {c: i for i, c in enumerate(_UPPER)}
_DICT2 = dict(enumerate(_UPPER))


def _make_full_key(message: str, key: str) -> str:
    """Cycle key to match message length."""
    key_cycle = (key * (len(message) // len(key) + 1))[:len(message)]
    return key_cycle


# ── Variant 1: dict lookup (original style) ───────────────────────────────────
def cipher_v1(message: str, key: str) -> str:
    key_full = _make_full_key(message.replace(" ", ""), key)
    out, ki = [], 0
    for letter in message:
        if letter == " ":
            out.append(" ")
        else:
            out.append(_DICT2[(_DICT1[letter] - _DICT1[key_full[ki]]) % 26])
            ki += 1
    return "".join(out)


# ── Variant 2: ord() arithmetic ──────────────────────────────────────────────
def cipher_v2(message: str, key: str) -> str:
    key_upper = key.upper()
    out, ki = [], 0
    for ch in message.upper():
        if ch == " ":
            out.append(" ")
        else:
            c = (ord(ch) - ord(key_upper[ki % len(key_upper)])) % 26 + 65
            out.append(chr(c))
            ki += 1
    return "".join(out)


# ── Variant 3: list comprehension with enumerate ──────────────────────────────
def cipher_v3(message: str, key: str) -> str:
    letters = [c for c in message.upper() if c.isalpha()]
    key_cycle = [key.upper()[i % len(key)] for i in range(len(letters))]
    result, li = [], 0
    for ch in message.upper():
        if ch.isalpha():
            result.append(chr((ord(ch) - ord(key_cycle[li])) % 26 + 65))
            li += 1
        else:
            result.append(ch)
    return "".join(result)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    msg = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG " * 5
    key = "SECRETKEY"
    n = 50_000

    setup = (
        f"from __main__ import cipher_v1, cipher_v2, cipher_v3; "
        f"m={msg!r}; k={key!r}"
    )
    print("=== Beaufort Cipher Benchmark (50k iterations) ===")
    for name, stmt in [
        ("cipher_v1 (dict lookup)", "cipher_v1(m, k)"),
        ("cipher_v2 (ord arith)", "cipher_v2(m, k)"),
        ("cipher_v3 (list comp)", "cipher_v3(m, k)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
