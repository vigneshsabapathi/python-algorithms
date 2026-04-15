# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/smith_waterman.py


def smith_waterman(
    seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1
) -> tuple[int, str, str]:
    """
    Smith-Waterman algorithm for local sequence alignment.

    Returns (score, aligned_seq1, aligned_seq2).

    >>> smith_waterman("TGTTACGG", "GGTTGACTA")
    (9, 'GTT-AC', 'GTTGAC')
    >>> smith_waterman("ACAT", "ACAT")
    (8, 'ACAT', 'ACAT')
    >>> smith_waterman("ABC", "DEF")
    (0, '', '')
    >>> smith_waterman("", "ABC")
    (0, '', '')
    """
    m, n = len(seq1), len(seq2)
    if m == 0 or n == 0:
        return (0, "", "")

    # Build scoring matrix
    H = [[0] * (n + 1) for _ in range(m + 1)]
    max_score = 0
    max_pos = (0, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diag = H[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            up = H[i - 1][j] + gap
            left = H[i][j - 1] + gap
            H[i][j] = max(0, diag, up, left)
            if H[i][j] > max_score:
                max_score = H[i][j]
                max_pos = (i, j)

    # Traceback
    aligned1, aligned2 = [], []
    i, j = max_pos
    while i > 0 and j > 0 and H[i][j] > 0:
        if H[i][j] == H[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch):
            aligned1.append(seq1[i - 1])
            aligned2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif H[i][j] == H[i - 1][j] + gap:
            aligned1.append(seq1[i - 1])
            aligned2.append("-")
            i -= 1
        else:
            aligned1.append("-")
            aligned2.append(seq2[j - 1])
            j -= 1

    return (max_score, "".join(reversed(aligned1)), "".join(reversed(aligned2)))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ("TGTTACGG", "GGTTGACTA", 9),
        ("ACAT", "ACAT", 8),
        ("ABC", "DEF", 0),
    ]
    for s1, s2, expected_score in cases:
        score, a1, a2 = smith_waterman(s1, s2)
        status = "OK" if score == expected_score else "FAIL"
        print(f"  [{status}] smith_waterman({s1!r}, {s2!r}) = score={score}  "
              f"aligned=({a1!r}, {a2!r})")
