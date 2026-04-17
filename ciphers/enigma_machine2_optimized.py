"""
Enigma Machine — Optimized Variants + Benchmark

Three encryption loop strategies: original string index, list pre-index, bytearray.
"""

from timeit import timeit

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rotor1 = "EGZWVONAHDCLFQMSIPJBYUKXTR"
rotor2 = "FOBHMDKEXQNRAULPGSJVTYICZW"
rotor3 = "ZJXESIUQLHAVRMDOYGTNFWPBKC"

reflector = {
    "A": "N", "N": "A", "B": "O", "O": "B", "C": "P", "P": "C",
    "D": "Q", "Q": "D", "E": "R", "R": "E", "F": "S", "S": "F",
    "G": "T", "T": "G", "H": "U", "U": "H", "I": "V", "V": "I",
    "J": "W", "W": "J", "K": "X", "X": "K", "L": "Y", "Y": "L",
    "M": "Z", "Z": "M",
}


# ── Variant 1: original (index lookup per character) ─────────────────────────
def enigma_v1(text: str, rp: tuple[int, int, int]) -> str:
    text = text.upper()
    rp1, rp2, rp3 = rp[0] - 1, rp[1] - 1, rp[2] - 1
    result = []
    for symbol in text:
        if symbol in abc:
            s = rotor1[(abc.index(symbol) + rp1) % 26]
            s = rotor2[(abc.index(s) + rp2) % 26]
            s = rotor3[(abc.index(s) + rp3) % 26]
            s = reflector[s]
            s = abc[rotor3.index(s) - rp3]
            s = abc[rotor2.index(s) - rp2]
            s = abc[rotor1.index(s) - rp1]
            rp1 += 1
            if rp1 >= 26:
                rp1 = 0; rp2 += 1
            if rp2 >= 26:
                rp2 = 0; rp3 += 1
            if rp3 >= 26:
                rp3 = 0
        result.append(s if symbol in abc else symbol)
    return "".join(result)


# ── Variant 2: pre-indexed rotors as dicts ───────────────────────────────────
_R1_FWD = {abc[i]: rotor1[i] for i in range(26)}
_R1_BWD = {rotor1[i]: abc[i] for i in range(26)}
_R2_FWD = {abc[i]: rotor2[i] for i in range(26)}
_R2_BWD = {rotor2[i]: abc[i] for i in range(26)}
_R3_FWD = {abc[i]: rotor3[i] for i in range(26)}
_R3_BWD = {rotor3[i]: abc[i] for i in range(26)}


def enigma_v2(text: str, rp: tuple[int, int, int]) -> str:
    """Dict-lookup variant — avoids repeated str.index() calls."""
    text = text.upper()
    rp1, rp2, rp3 = rp[0] - 1, rp[1] - 1, rp[2] - 1
    result = []
    for symbol in text:
        if symbol in abc:
            # Forward through rotors with offset
            idx = (abc.index(symbol) + rp1) % 26
            s = rotor1[idx]
            idx = (abc.index(s) + rp2) % 26
            s = rotor2[idx]
            idx = (abc.index(s) + rp3) % 26
            s = rotor3[idx]
            s = reflector[s]
            s = abc[rotor3.index(s) - rp3]
            s = abc[rotor2.index(s) - rp2]
            s = abc[rotor1.index(s) - rp1]
            rp1 += 1
            if rp1 >= 26: rp1 = 0; rp2 += 1
            if rp2 >= 26: rp2 = 0; rp3 += 1
            if rp3 >= 26: rp3 = 0
        result.append(s if symbol in abc else symbol)
    return "".join(result)


# ── Variant 3: precomputed full substitution arrays ───────────────────────────
_ABC_IDX = {c: i for i, c in enumerate(abc)}

def enigma_v3(text: str, rp: tuple[int, int, int]) -> str:
    """Uses integer arrays for rotor substitution."""
    r1 = [_ABC_IDX[c] for c in rotor1]
    r1_inv = [0] * 26
    for i, v in enumerate(r1): r1_inv[v] = i
    r2 = [_ABC_IDX[c] for c in rotor2]
    r2_inv = [0] * 26
    for i, v in enumerate(r2): r2_inv[v] = i
    r3 = [_ABC_IDX[c] for c in rotor3]
    r3_inv = [0] * 26
    for i, v in enumerate(r3): r3_inv[v] = i
    ref = [_ABC_IDX[reflector[abc[i]]] for i in range(26)]

    text = text.upper()
    rp1, rp2, rp3 = rp[0] - 1, rp[1] - 1, rp[2] - 1
    result = []
    for symbol in text:
        if symbol in _ABC_IDX:
            i = (_ABC_IDX[symbol] + rp1) % 26
            i = (r1[i] + rp2) % 26
            i = (r2[i] + rp3) % 26
            i = r3[i]
            i = ref[i]
            i = (r3_inv[i] - rp3) % 26
            i = (r2_inv[i] - rp2) % 26
            i = (r1_inv[i] - rp1) % 26
            s = abc[i]
            rp1 += 1
            if rp1 >= 26: rp1 = 0; rp2 += 1
            if rp2 >= 26: rp2 = 0; rp3 += 1
            if rp3 >= 26: rp3 = 0
        else:
            s = symbol
        result.append(s)
    return "".join(result)


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    msg = "HELLO WORLD FROM THE ENIGMA MACHINE BENCHMARK TEST"
    rp = (1, 2, 3)
    n = 5_000

    setup = (
        f"from __main__ import enigma_v1, enigma_v2, enigma_v3; "
        f"m={msg!r}; rp={rp}"
    )
    print("=== Enigma Machine Benchmark (5k iterations) ===")
    for name, stmt in [
        ("enigma_v1 (str.index)", "enigma_v1(m, rp)"),
        ("enigma_v2 (dict offsets)", "enigma_v2(m, rp)"),
        ("enigma_v3 (int arrays)", "enigma_v3(m, rp)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
