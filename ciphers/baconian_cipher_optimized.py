"""
Baconian Cipher — Optimized Variants + Benchmark

Three encoding strategies: dict lookup, list comprehension, bytes join.
"""

from timeit import timeit

ENCODE_DICT: dict[str, str] = {
    "a": "AAAAA", "b": "AAAAB", "c": "AAABA", "d": "AAABB", "e": "AABAA",
    "f": "AABAB", "g": "AABBA", "h": "AABBB", "i": "ABAAA", "j": "BBBAA",
    "k": "ABAAB", "l": "ABABA", "m": "ABABB", "n": "ABBAA", "o": "ABBAB",
    "p": "ABBBA", "q": "ABBBB", "r": "BAAAA", "s": "BAAAB", "t": "BAABA",
    "u": "BAABB", "v": "BBBAB", "w": "BABAA", "x": "BABAB", "y": "BABBA",
    "z": "BABBB", " ": " ",
}
DECODE_DICT: dict[str, str] = {v: k for k, v in ENCODE_DICT.items()}


# ── Variant 1: simple dict join (original) ───────────────────────────────────
def encode_v1(word: str) -> str:
    return "".join(ENCODE_DICT[c] for c in word.lower())


# ── Variant 2: list accumulation ─────────────────────────────────────────────
def encode_v2(word: str) -> str:
    parts = []
    for c in word.lower():
        parts.append(ENCODE_DICT[c])
    return "".join(parts)


# ── Variant 3: map() functional ──────────────────────────────────────────────
def encode_v3(word: str) -> str:
    return "".join(map(ENCODE_DICT.__getitem__, word.lower()))


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    sample = "hello world from the baconian cipher algorithm " * 3
    n = 100_000

    setup = (
        f"from __main__ import encode_v1, encode_v2, encode_v3; s={sample!r}"
    )
    print("=== Baconian Cipher Benchmark (100k iterations) ===")
    for name, stmt in [
        ("encode_v1 (generator join)", "encode_v1(s)"),
        ("encode_v2 (list append)", "encode_v2(s)"),
        ("encode_v3 (map)", "encode_v3(s)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
