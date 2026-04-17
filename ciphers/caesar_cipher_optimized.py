"""
Caesar Cipher — Optimized Variants + Benchmark

Three encryption strategies: index-based, ord() arithmetic, str.translate.
"""

from string import ascii_letters
from timeit import timeit


# ── Variant 1: index-based (original) ────────────────────────────────────────
def encrypt_v1(text: str, key: int, alphabet: str = ascii_letters) -> str:
    result = []
    for ch in text:
        if ch in alphabet:
            result.append(alphabet[(alphabet.index(ch) + key) % len(alphabet)])
        else:
            result.append(ch)
    return "".join(result)


# ── Variant 2: ord() arithmetic (uppercase-only fast path) ───────────────────
def encrypt_v2(text: str, key: int) -> str:
    """Faster when alphabet is standard ASCII letters (upper + lower)."""
    result = []
    for ch in text:
        o = ord(ch)
        if 65 <= o <= 90:
            result.append(chr((o - 65 + key) % 26 + 65))
        elif 97 <= o <= 122:
            result.append(chr((o - 97 + key) % 26 + 97))
        else:
            result.append(ch)
    return "".join(result)


# ── Variant 3: str.translate ──────────────────────────────────────────────────
def _make_caesar_table(key: int) -> dict[int, int]:
    import string
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    shifted_upper = upper[key % 26 :] + upper[: key % 26]
    shifted_lower = lower[key % 26 :] + lower[: key % 26]
    return str.maketrans(upper + lower, shifted_upper + shifted_lower)


def encrypt_v3(text: str, key: int) -> str:
    """str.translate — O(n) with C-level table lookup."""
    return text.translate(_make_caesar_table(key))


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    msg = "The quick brown fox jumps over the lazy dog. " * 10
    key = 13
    n = 50_000

    setup = (
        f"from __main__ import encrypt_v1, encrypt_v2, encrypt_v3, _make_caesar_table; "
        f"m={msg!r}; k={key}; t=_make_caesar_table(k)"
    )
    print("=== Caesar Cipher Benchmark (50k iterations) ===")
    for name, stmt in [
        ("encrypt_v1 (index)", "encrypt_v1(m, k)"),
        ("encrypt_v2 (ord arith)", "encrypt_v2(m, k)"),
        ("encrypt_v3 (translate)", "encrypt_v3(m, k)"),
        ("encrypt_v3 (cached table)", "m.translate(t)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
