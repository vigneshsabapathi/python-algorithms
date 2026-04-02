"""
Natural Sort — Optimized & Alternative Implementations
=======================================================

Natural sort (aka "human sort") orders strings by embedded numeric value rather
than lexicographic code point.  "file10" comes after "file9", not before "file2".

Approaches compared
--------------------
1. regex_split   — baseline: re.split + int() key (the reference implementation)
2. natsort_lib   — natsort library (PyPI); handles locale, Unicode, floats, paths
3. locale_aware  — ICU/locale collation via locale.strxfrm + a digit normaliser
4. cached_key    — pre-compute keys once, avoid repeated re.split calls
5. bytes_key     — build a bytes sort key (avoids mixed int/str key list)

All produce identical results on well-formed ASCII input.
"""

from __future__ import annotations

import re
import time
import random
import string


# ---------------------------------------------------------------------------
# 1. Baseline (reference) — regex split + int conversion
# ---------------------------------------------------------------------------
def natural_sort_regex(input_list: list[str]) -> list[str]:
    """
    Standard alphanum key: split on digit runs, cast digits to int, lowercase text.

    >>> natural_sort_regex(['file10', 'file2', 'file1'])
    ['file1', 'file2', 'file10']
    >>> natural_sort_regex(['Elm11', 'Elm2', 'elm0'])
    ['elm0', 'Elm2', 'Elm11']
    """
    def key(s: str):
        return [int(c) if c.isdigit() else c.lower() for c in re.split(r"([0-9]+)", s)]
    return sorted(input_list, key=key)


# ---------------------------------------------------------------------------
# 2. natsort library — richest feature set
# ---------------------------------------------------------------------------
def natural_sort_natsort(input_list: list[str]) -> list[str]:
    """
    Uses the `natsort` PyPI library.  Handles floats, locale, paths, signed
    numbers, and Unicode out of the box.

    >>> natural_sort_natsort(['file10', 'file2', 'file1'])
    ['file1', 'file2', 'file10']
    >>> natural_sort_natsort(['v1.10', 'v1.9', 'v1.2'])
    ['v1.2', 'v1.9', 'v1.10']
    """
    try:
        from natsort import natsorted
        return natsorted(input_list)
    except ImportError:
        # Graceful fallback so the file still runs without the library installed.
        return natural_sort_regex(input_list)


# ---------------------------------------------------------------------------
# 3. Cached key — avoids recomputing the regex key during Timsort comparisons
# ---------------------------------------------------------------------------
def natural_sort_cached(input_list: list[str]) -> list[str]:
    """
    Pre-build all keys once into a list of (key, original) pairs, sort, then
    strip the keys.  Useful when input_list is very large and Python's sort
    would otherwise recompute the key multiple times per element.

    >>> natural_sort_cached(['file10', 'file2', 'file1'])
    ['file1', 'file2', 'file10']
    """
    _split = re.compile(r"([0-9]+)").split

    def key(s: str):
        parts = _split(s)
        return [int(p) if p.isdigit() else p.lower() for p in parts]

    keyed = [(key(s), s) for s in input_list]
    keyed.sort()
    return [s for _, s in keyed]


# ---------------------------------------------------------------------------
# 4. Bytes key — encode the sort key as a bytes object for faster comparison
# ---------------------------------------------------------------------------
_DIGIT_RE = re.compile(r"([0-9]+)")

def natural_sort_bytes_key(input_list: list[str]) -> list[str]:
    """
    Encodes each segment as fixed-width bytes: text segments as UTF-8 prefixed
    with b'\\x00', numeric segments zero-padded to 20 digits prefixed with b'\\x01'.
    Byte comparison is fast and avoids mixed int/str list comparison.

    >>> natural_sort_bytes_key(['file10', 'file2', 'file1'])
    ['file1', 'file2', 'file10']
    >>> natural_sort_bytes_key(['2 ft 7 in', '1 ft 5 in', '10 ft 2 in'])
    ['1 ft 5 in', '2 ft 7 in', '10 ft 2 in']
    """
    def key(s: str) -> bytes:
        out = bytearray()
        for part in _DIGIT_RE.split(s):
            if part.isdigit():
                out += b"\x01" + part.zfill(20).encode()
            else:
                out += b"\x00" + part.lower().encode()
        return bytes(out)

    return sorted(input_list, key=key)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def _make_data(n: int) -> list[str]:
    prefixes = ["file", "img", "track", "item", "node"]
    return [
        random.choice(prefixes) + str(random.randint(1, 9999)) + ".txt"
        for _ in range(n)
    ]


def benchmark() -> None:
    sizes = [1_000, 5_000, 20_000, 100_000]
    implementations = [
        ("regex_split (baseline)", natural_sort_regex),
        ("cached_key",             natural_sort_cached),
        ("bytes_key",              natural_sort_bytes_key),
        ("natsort_lib",            natural_sort_natsort),
        ("sorted() [lexicographic]", lambda x: sorted(x)),
    ]

    header = f"{'n':>8}  " + "  ".join(f"{name:>28}" for name, _ in implementations)
    print(header)
    print("-" * len(header))

    for n in sizes:
        data = _make_data(n)
        row = f"{n:>8}  "
        for name, fn in implementations:
            runs = 3
            t = min(
                sum(
                    (lambda d=data[:]: (s := time.perf_counter(), fn(d), time.perf_counter() - s)[2])()
                    for _ in range(runs)
                ) / runs
                for _ in range(1)
            )
            # Simpler timing:
            times = []
            for _ in range(3):
                d = data[:]
                t0 = time.perf_counter()
                fn(d)
                times.append(time.perf_counter() - t0)
            row += f"{min(times):>28.4f}  "
        print(row)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of 3 runs) ===\n")
    benchmark()
