"""
Trifid Cipher — Optimized Variants & Benchmark
================================================
Three implementations of Trifid encrypt_message.
"""

import timeit

TEST_CHAR_TO_NUM = {
    "A": "111", "B": "112", "C": "113", "D": "121", "E": "122", "F": "123", "G": "131",
    "H": "132", "I": "133", "J": "211", "K": "212", "L": "213", "M": "221", "N": "222",
    "O": "223", "P": "231", "Q": "232", "R": "233", "S": "311", "T": "312", "U": "313",
    "V": "321", "W": "322", "X": "323", "Y": "331", "Z": "332", ".": "333",
}
TEST_NUM_TO_CHAR = {v: k for k, v in TEST_CHAR_TO_NUM.items()}


def _make_dicts(alphabet: str) -> tuple[dict[str, str], dict[str, str]]:
    alphabet = alphabet.replace(" ", "").upper()
    c2n = dict(zip(alphabet, TEST_CHAR_TO_NUM.values()))
    n2c = {v: k for k, v in c2n.items()}
    return c2n, n2c


# Variant 1: String concatenation per-character
def encrypt_v1(message: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.", period: int = 5) -> str:
    msg = message.replace(" ", "").upper()
    c2n, n2c = _make_dicts(alphabet)
    enc_num = ""
    for i in range(0, len(msg) + 1, period):
        part = msg[i : i + period]
        one = two = three = ""
        for c in (c2n[x] for x in part):
            one += c[0]; two += c[1]; three += c[2]
        enc_num += one + two + three
    return "".join(n2c[enc_num[i : i + 3]] for i in range(0, len(enc_num), 3))


# Variant 2: List-based (avoids repeated string concat)
def encrypt_v2(message: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.", period: int = 5) -> str:
    msg = message.replace(" ", "").upper()
    c2n, n2c = _make_dicts(alphabet)
    enc_num: list[str] = []
    for i in range(0, len(msg) + 1, period):
        part = msg[i : i + period]
        rows: list[list[str]] = [[], [], []]
        for c in part:
            tri = c2n[c]
            rows[0].append(tri[0])
            rows[1].append(tri[1])
            rows[2].append(tri[2])
        enc_num.extend(rows[0] + rows[1] + rows[2])
    joined = "".join(enc_num)
    return "".join(n2c[joined[i : i + 3]] for i in range(0, len(joined), 3))


# Variant 3: Integer-based (store trigrams as ints, avoid string slicing)
def encrypt_v3(message: str, alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.", period: int = 5) -> str:
    msg = message.replace(" ", "").upper()
    c2n, n2c = _make_dicts(alphabet)
    # Pre-convert all chars to 3-int tuples
    c2t = {c: (int(v[0]), int(v[1]), int(v[2])) for c, v in c2n.items()}
    out_chars: list[str] = []
    for i in range(0, len(msg) + 1, period):
        part = msg[i : i + period]
        if not part:
            break
        trigs = [c2t[c] for c in part]
        enc = (
            [t[0] for t in trigs]
            + [t[1] for t in trigs]
            + [t[2] for t in trigs]
        )
        for j in range(0, len(enc), 3):
            key_str = str(enc[j]) + str(enc[j + 1]) + str(enc[j + 2])
            out_chars.append(n2c[key_str])
    return "".join(out_chars)


def benchmark(n: int = 20_000) -> None:
    setup = (
        "from __main__ import encrypt_v1, encrypt_v2, encrypt_v3; "
        "msg = 'DEFEND THE EAST WALL OF THE CASTLE'"
    )
    t1 = timeit.timeit("encrypt_v1(msg)", setup=setup, number=n)
    t2 = timeit.timeit("encrypt_v2(msg)", setup=setup, number=n)
    t3 = timeit.timeit("encrypt_v3(msg)", setup=setup, number=n)
    print(f"V1 (str concat) : {t1:.4f}s for {n:,} runs")
    print(f"V2 (list-based) : {t2:.4f}s for {n:,} runs")
    print(f"V3 (int-based)  : {t3:.4f}s for {n:,} runs")


if __name__ == "__main__":
    msg = "DEFEND THE EAST WALL"
    print("V1:", encrypt_v1(msg))
    print("V2:", encrypt_v2(msg))
    print("V3:", encrypt_v3(msg))
    print()
    benchmark()
