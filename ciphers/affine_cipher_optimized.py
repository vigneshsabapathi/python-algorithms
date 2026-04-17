"""
Affine Cipher — Optimized Variants + Benchmark

Three encryption implementation strategies for the affine cipher.
"""

from math import gcd
from timeit import timeit

SYMBOLS = (
    r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"""
    r"""abcdefghijklmnopqrstuvwxyz{|}~"""
)
M = len(SYMBOLS)


def _find_mod_inverse(a: int, m: int) -> int:
    if gcd(a, m) != 1:
        raise ValueError(f"mod inverse of {a} and {m} does not exist")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = u1 - q * v1, u2 - q * v2, u3 - q * v3, v1, v2, v3
    return u1 % m


# ── Variant 1: character-by-character (original) ──────────────────────────────
def encrypt_v1(message: str, key_a: int, key_b: int) -> str:
    """Original per-char approach using str.find()."""
    return "".join(
        SYMBOLS[(SYMBOLS.find(c) * key_a + key_b) % M] if c in SYMBOLS else c
        for c in message
    )


# ── Variant 2: precompute translation table ───────────────────────────────────
def _make_encrypt_table(key_a: int, key_b: int) -> dict[str, str]:
    return {SYMBOLS[i]: SYMBOLS[(i * key_a + key_b) % M] for i in range(M)}


def encrypt_v2(message: str, key_a: int, key_b: int) -> str:
    """Pre-built lookup table (good when same key is reused many times)."""
    table = _make_encrypt_table(key_a, key_b)
    return "".join(table.get(c, c) for c in message)


# ── Variant 3: str.translate with ordinal table ───────────────────────────────
def _make_str_translate_table(key_a: int, key_b: int) -> dict[int, str]:
    return {
        ord(SYMBOLS[i]): SYMBOLS[(i * key_a + key_b) % M]
        for i in range(M)
    }


def encrypt_v3(message: str, key_a: int, key_b: int) -> str:
    """str.translate() — fastest for pure-symbol strings."""
    table = _make_str_translate_table(key_a, key_b)
    return message.translate(table)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    key_a, key_b = 47, 12
    msg = "The affine cipher is a type of monoalphabetic substitution cipher." * 5
    n = 50_000

    setup = (
        f"from __main__ import encrypt_v1, encrypt_v2, encrypt_v3, "
        f"_make_encrypt_table, _make_str_translate_table; "
        f"ka={key_a}; kb={key_b}; msg={msg!r}; "
        f"t2=_make_encrypt_table(ka, kb); t3=_make_str_translate_table(ka, kb)"
    )

    print("=== Affine Cipher Benchmark (50k iterations) ===")
    for name, stmt in [
        ("encrypt_v1 (find)", "encrypt_v1(msg, ka, kb)"),
        ("encrypt_v2 (dict)", "encrypt_v2(msg, ka, kb)"),
        ("encrypt_v3 (translate)", "encrypt_v3(msg, ka, kb)"),
        ("encrypt_v3 (cached table)", "msg.translate(t3)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
