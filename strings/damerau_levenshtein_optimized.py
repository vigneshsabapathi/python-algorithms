"""
Optimized Damerau-Levenshtein implementations.
Companion to damerau_levenshtein_distance.py.

Three variants:
  1. OSA rolling-array  — same OSA semantics, O(min(n,m)) space instead of O(n*m)
  2. True DL            — full Damerau-Levenshtein, allows multi-step transpositions
  3. Benchmark          — compares all three (OSA original, OSA rolling, true DL)

Key difference between OSA and true DL:
  damerau_levenshtein_distance("CA", "ABC")  -> OSA=3, True DL=2
  The true DL can "CA"→"AC"→"ABC" in 2 ops; OSA forbids editing a substring twice.
"""

from collections import defaultdict


# ---------------------------------------------------------------------------
# 1. OSA rolling-array — O(min(n,m)) space
# ---------------------------------------------------------------------------

def osa_rolling(s1: str, s2: str) -> int:
    """
    OSA distance using only three rows instead of a full n×m matrix.
    Same result as the original for all inputs.

    >>> osa_rolling("cat", "cut")
    1
    >>> osa_rolling("kitten", "sitting")
    3
    >>> osa_rolling("ab", "ba")
    1
    >>> osa_rolling("CA", "ABC")
    3
    >>> osa_rolling("", "abc")
    3
    >>> osa_rolling("abc", "")
    3
    >>> osa_rolling("", "")
    0
    """
    # Always iterate over the longer string to keep the shorter one as columns
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    m = len(s2)
    # Three rows: prev_prev (i-2), prev (i-1), curr (i)
    prev_prev = list(range(m + 1))
    prev      = list(range(m + 1))
    curr      = [0] * (m + 1)

    for i, c1 in enumerate(s1, start=1):
        curr[0] = i
        for j, c2 in enumerate(s2, start=1):
            cost = int(c1 != c2)
            curr[j] = min(
                prev[j] + 1,       # deletion
                curr[j - 1] + 1,   # insertion
                prev[j - 1] + cost, # substitution
            )
            # Transposition check
            if (
                i > 1
                and j > 1
                and s1[i - 1] == s2[j - 2]
                and s1[i - 2] == s2[j - 1]
            ):
                curr[j] = min(curr[j], prev_prev[j - 2] + cost)

        prev_prev, prev, curr = prev, curr, [0] * (m + 1)

    return prev[m]


# ---------------------------------------------------------------------------
# 2. True Damerau-Levenshtein (unrestricted)
# ---------------------------------------------------------------------------

def true_damerau_levenshtein(s1: str, s2: str) -> int:
    """
    True Damerau-Levenshtein distance — allows a substring to be edited more
    than once, so it correctly handles non-adjacent transpositions.

    Differs from OSA only when a transposition sequence requires intermediate edits:
      "CA" → "ABC": OSA=3, True DL=2

    >>> true_damerau_levenshtein("cat", "cut")
    1
    >>> true_damerau_levenshtein("kitten", "sitting")
    3
    >>> true_damerau_levenshtein("ab", "ba")
    1
    >>> true_damerau_levenshtein("CA", "ABC")
    2
    >>> true_damerau_levenshtein("", "abc")
    3
    >>> true_damerau_levenshtein("abc", "")
    3
    >>> true_damerau_levenshtein("", "")
    0
    """
    n, m = len(s1), len(s2)
    # Alphabet of all characters present in either string
    alphabet = set(s1) | set(s2)

    # last_row[c] = last row index where character c appeared in s1
    last_row: dict[str, int] = defaultdict(int)

    # dp[i][j] with sentinel border of size n+2 × m+2
    # Offset by 1: dp[i+1][j+1] corresponds to s1[:i], s2[:j]
    inf = n + m + 1
    dp = [[inf] * (m + 2) for _ in range(n + 2)]
    dp[0][0] = inf
    for i in range(n + 1):
        dp[i + 1][0] = inf
        dp[i + 1][1] = i
    for j in range(m + 1):
        dp[0][j + 1] = inf
        dp[1][j + 1] = j

    for i, c1 in enumerate(s1, start=1):
        last_col = 0  # last column index where s1[i-1] appeared in s2

        for j, c2 in enumerate(s2, start=1):
            i2 = last_row[c2]  # last row in s1 where s2[j-1] appeared
            j2 = last_col      # last col in s2 where s1[i-1] appeared
            cost = int(c1 != c2)

            dp[i + 1][j + 1] = min(
                dp[i][j] + cost,         # substitution / match
                dp[i + 1][j] + 1,        # insertion
                dp[i][j + 1] + 1,        # deletion
                # True transposition: jump from (i2-1, j2-1) over the swapped block
                dp[i2][j2] + (i - i2 - 1) + 1 + (j - j2 - 1),
            )

            if c1 == c2:
                last_col = j  # s1[i-1] last seen at column j in s2

        last_row[c1] = i  # s1[i-1] last seen at row i

    return dp[n + 1][m + 1]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    from timeit import timeit
    from damerau_levenshtein_distance import damerau_levenshtein_distance

    n = 50_000
    pairs = [
        ("kitten", "sitting"),
        ("The quick brown fox", "The slow green cat"),
        ("Damerau", "Levenshtein"),
    ]

    print(f"Benchmarking {n:,} runs per pair:\n")
    for s1, s2 in pairs:
        label = f'("{s1}", "{s2}")'

        t_orig = timeit(
            "damerau_levenshtein_distance(s1, s2)",
            setup=f"from damerau_levenshtein_distance import damerau_levenshtein_distance; s1={s1!r}; s2={s2!r}",
            number=n,
        )
        t_roll = timeit(
            "osa_rolling(s1, s2)",
            setup=f"from damerau_levenshtein_optimized import osa_rolling; s1={s1!r}; s2={s2!r}",
            number=n,
        )
        t_true = timeit(
            "true_damerau_levenshtein(s1, s2)",
            setup=f"from damerau_levenshtein_optimized import true_damerau_levenshtein; s1={s1!r}; s2={s2!r}",
            number=n,
        )

        print(f"  {label}")
        print(f"    OSA original  (full matrix)   {t_orig:.4f}s")
        print(f"    OSA rolling   (3-row space)   {t_roll:.4f}s")
        print(f"    True DL       (unrestricted)  {t_true:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
