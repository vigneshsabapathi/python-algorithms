"""
Bifid Cipher — Optimized Variants + Benchmark

Three encode strategies: numpy (original), pure-dict, pure-list.
"""

from timeit import timeit

# 5x5 Polybius square (j merged with i)
SQUARE_FLAT = ["a","b","c","d","e","f","g","h","i","k",
               "l","m","n","o","p","q","r","s","t","u",
               "v","w","x","y","z"]

# Pure-Python lookup dicts: letter -> (row, col) 1-indexed
_LETTER_TO_RC: dict[str, tuple[int, int]] = {
    ch: (i // 5 + 1, i % 5 + 1)
    for i, ch in enumerate(SQUARE_FLAT)
}
_RC_TO_LETTER: dict[tuple[int, int], str] = {v: k for k, v in _LETTER_TO_RC.items()}


# ── Variant 1: numpy-based (original) ────────────────────────────────────────
def encode_v1(message: str) -> str:
    import numpy as np
    sq = np.array([list(SQUARE_FLAT[i*5:(i+1)*5]) for i in range(5)])
    message = message.lower().replace(" ", "").replace("j", "i")
    rows, cols = [], []
    for ch in message:
        r, c = np.where(ch == sq)
        rows.append(int(r[0]) + 1)
        cols.append(int(c[0]) + 1)
    combined = rows + cols
    enc = ""
    for i in range(len(message)):
        enc += _RC_TO_LETTER[(combined[i * 2], combined[i * 2 + 1])]
    return enc


# ── Variant 2: pure-Python dict ───────────────────────────────────────────────
def encode_v2(message: str) -> str:
    msg = message.lower().replace(" ", "").replace("j", "i")
    rows = [_LETTER_TO_RC[ch][0] for ch in msg]
    cols = [_LETTER_TO_RC[ch][1] for ch in msg]
    n = len(msg)
    combined = rows + cols
    return "".join(
        _RC_TO_LETTER[(combined[2 * i], combined[2 * i + 1])]
        for i in range(n)
    )


# ── Variant 3: array-based (no numpy) ────────────────────────────────────────
def encode_v3(message: str) -> str:
    msg = message.lower().replace(" ", "").replace("j", "i")
    n = len(msg)
    pairs = [_LETTER_TO_RC[ch] for ch in msg]
    flat = [v for r, c in pairs for v in (r, c)]
    return "".join(
        _RC_TO_LETTER[(flat[2 * i], flat[2 * i + 1])]
        for i in range(n)
    )


def decode_v2(message: str) -> str:
    msg = message.lower().replace(" ", "")
    n = len(msg)
    flat = [v for ch in msg for v in _LETTER_TO_RC[ch]]
    rows = flat[:n]
    cols = flat[n:]
    return "".join(_RC_TO_LETTER[(rows[i], cols[i])] for i in range(n))


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    msg = "testmessage" * 5
    n = 10_000

    setup = f"from __main__ import encode_v1, encode_v2, encode_v3; m={msg!r}"
    print("=== Bifid Cipher Benchmark (10k iterations) ===")
    for name, stmt in [
        ("encode_v1 (numpy)", "encode_v1(m)"),
        ("encode_v2 (pure dict)", "encode_v2(m)"),
        ("encode_v3 (flat array)", "encode_v3(m)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
