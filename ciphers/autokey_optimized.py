"""
Autokey Cipher — Optimized Variants + Benchmark

Three encrypt/decrypt strategies with varying loop styles.
"""

from timeit import timeit


# ── Variant 1: original while-loop style ─────────────────────────────────────
def encrypt_v1(plaintext: str, key: str) -> str:
    """Original while-loop implementation."""
    key = (key + plaintext).lower()
    plaintext = plaintext.lower()
    pt_i = ki = 0
    out = []
    while pt_i < len(plaintext):
        p = ord(plaintext[pt_i])
        if p < 97 or p > 122:
            out.append(plaintext[pt_i])
            pt_i += 1
        elif ord(key[ki]) < 97 or ord(key[ki]) > 122:
            ki += 1
        else:
            out.append(chr((p - 97 + ord(key[ki]) - 97) % 26 + 97))
            ki += 1
            pt_i += 1
    return "".join(out)


# ── Variant 2: generator using zip + filter ───────────────────────────────────
def encrypt_v2(plaintext: str, key: str) -> str:
    """Generator-based approach building key lazily."""
    pt = plaintext.lower()
    full_key = (key + plaintext).lower()
    out = []
    ki = 0
    for ch in pt:
        if ch.isalpha():
            # skip non-alpha key chars
            while not full_key[ki].isalpha():
                ki += 1
            out.append(chr((ord(ch) - 97 + ord(full_key[ki]) - 97) % 26 + 97))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# ── Variant 3: list + index arithmetic ───────────────────────────────────────
def encrypt_v3(plaintext: str, key: str) -> str:
    """List-based: filter alpha-only key, then zip."""
    pt_lower = plaintext.lower()
    key_alpha = [c for c in (key + plaintext).lower() if c.isalpha()]
    out = []
    ki = 0
    for ch in pt_lower:
        if ch.isalpha():
            out.append(chr((ord(ch) - 97 + ord(key_alpha[ki])) % 26 + 97))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    plain = "the quick brown fox jumps over the lazy dog " * 5
    key = "secretkey"
    n = 50_000

    setup = (
        f"from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        f"p={plain!r}; k={key!r}"
    )
    print("=== Autokey Cipher Benchmark (50k iterations) ===")
    for name, stmt in [
        ("encrypt_v1 (while loop)", "encrypt_v1(p, k)"),
        ("encrypt_v2 (for + alpha check)", "encrypt_v2(p, k)"),
        ("encrypt_v3 (pre-filter key)", "encrypt_v3(p, k)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
