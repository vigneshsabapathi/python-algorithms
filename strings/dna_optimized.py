"""
Optimized DNA complement implementations.
Companion to dna.py — see that file for the regex-based baseline.

The complement of a DNA strand maps: A<->T, C<->G.
"""

# Pre-build the translation table once at module level — reused on every call
_COMPLEMENT_TABLE = str.maketrans("ATCG", "TAGC")
_VALID_BASES = frozenset("ATCG")


def dna_set(strand: str) -> str:
    """
    Validates with a frozenset check instead of regex — no re import.
    Uses the same maketrans/translate for the complement (C-level, fastest).

    >>> dna_set("GCTA")
    'CGAT'
    >>> dna_set("ATGC")
    'TACG'
    >>> dna_set("CTGA")
    'GACT'
    >>> dna_set("")
    ''
    >>> dna_set("GFGG")
    Traceback (most recent call last):
        ...
    ValueError: Invalid Strand
    """
    if not all(c in _VALID_BASES for c in strand):
        raise ValueError("Invalid Strand")
    return strand.translate(_COMPLEMENT_TABLE)


def dna_dict(strand: str) -> str:
    """
    Uses a dict lookup + join — more explicit but slower than translate().

    >>> dna_dict("GCTA")
    'CGAT'
    >>> dna_dict("ATGC")
    'TACG'
    >>> dna_dict("CTGA")
    'GACT'
    >>> dna_dict("")
    ''
    >>> dna_dict("GFGG")
    Traceback (most recent call last):
        ...
    ValueError: Invalid Strand
    """
    _complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
    if not all(c in _complement for c in strand):
        raise ValueError("Invalid Strand")
    return "".join(_complement[c] for c in strand)


def benchmark() -> None:
    """Benchmark all three DNA complement implementations."""
    from timeit import timeit

    n = 200_000
    strand = "ATCGATCGATCG"  # 12-base strand

    cases = [
        (f'dna("{strand}")',
         "from dna import dna",
         "regex + translate (original)"),
        (f'dna_set("{strand}")',
         "from dna_optimized import dna_set",
         "frozenset + translate (optimized)"),
        (f'dna_dict("{strand}")',
         "from dna_optimized import dna_dict",
         "dict + join        (optimized)"),
    ]

    print(f"Benchmarking {n:,} runs on '{strand}':\n")
    for stmt, setup, label in cases:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {label:<35} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
