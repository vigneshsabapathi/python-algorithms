"""Optimized and alternative implementations of Shell Sort.

Shell sort's performance is almost entirely determined by its gap sequence.
Different sequences give different worst-case complexities and real-world speeds.

Gap sequences compared:
1. Shrink 1.3  (original — Tokuda-adjacent, good average behaviour)
2. Shell 1959  (n/2, n/4 ... 1) — original Shell gaps, O(n²) worst case
3. Knuth 1973  (1, 4, 13, 40, 121 ...) — O(n^1.5), classic interview answer
4. Ciura 2001  (1,4,10,23,57,132,301,701,...) — empirically best known sequence
5. Tokuda 1992 (1,4,9,20,46,103,...) — closed-form, nearly as good as Ciura
6. sorted() built-in — Timsort reference

References:
  https://en.wikipedia.org/wiki/Shellsort#Gap_sequences
"""

from __future__ import annotations
import time
import random


# ---------------------------------------------------------------------------
# Core shell sort engine — takes a pre-computed gap list (largest first)
# ---------------------------------------------------------------------------
def _shell_sort_with_gaps(arr: list, gaps: list[int]) -> list:
    for gap in gaps:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
    return arr


# ---------------------------------------------------------------------------
# Gap sequence generators
# ---------------------------------------------------------------------------
def _gaps_shrink13(n: int) -> list[int]:
    """Shrink-by-1.3 (original): starts at n, divides by 1.3 each step."""
    gaps = []
    gap = n
    while gap > 1:
        gap = int(gap / 1.3)
        gaps.append(max(gap, 1))
    return gaps


def _gaps_shell(n: int) -> list[int]:
    """Shell 1959: n//2, n//4, ..., 1  — simplest, O(n²) worst case."""
    gaps = []
    gap = n // 2
    while gap > 0:
        gaps.append(gap)
        gap //= 2
    return gaps


def _gaps_knuth(n: int) -> list[int]:
    """Knuth 1973: (3^k - 1) / 2 → 1, 4, 13, 40, 121 ...  O(n^1.5)."""
    gap, gaps = 1, []
    while gap < n // 3:
        gap = gap * 3 + 1
    while gap >= 1:
        gaps.append(gap)
        gap //= 3
    return gaps


def _gaps_ciura(n: int) -> list[int]:
    """Ciura 2001: empirically optimal known sequence up to 1750.
    Extended with *2.25 factor beyond that."""
    base = [1, 4, 10, 23, 57, 132, 301, 701, 1750]
    gap = 1750
    while gap < n:
        gap = int(gap * 2.25)
        base.append(gap)
    return [g for g in reversed(base) if g < n]


def _gaps_tokuda(n: int) -> list[int]:
    """Tokuda 1992: h_k = ceil((9*(9/4)^k - 4) / 5), k=1,2,...
    Closed-form formula, nearly as good as Ciura empirically.
    Always ends with gap=1 to guarantee a complete insertion-sort pass."""
    gaps = []
    k = 1
    while True:
        gap = int((9 * (9 / 4) ** k - 4) / 5 + 0.5)
        if gap >= n:
            break
        gaps.append(gap)
        k += 1
    result = list(reversed(gaps))
    # Always ensure the final pass is gap=1
    if not result or result[-1] != 1:
        result.append(1)
    return result


# ---------------------------------------------------------------------------
# Public sort functions
# ---------------------------------------------------------------------------
def shell_sort_shrink13(collection: list) -> list:
    """Original shrink-1.3 shell sort.

    >>> shell_sort_shrink13([3, 2, 1])
    [1, 2, 3]
    >>> shell_sort_shrink13([])
    []
    >>> shell_sort_shrink13([5, 1, 9, 3, 7])
    [1, 3, 5, 7, 9]
    """
    a = list(collection)
    return _shell_sort_with_gaps(a, _gaps_shrink13(len(a)))


def shell_sort_shell(collection: list) -> list:
    """Shell 1959 gaps (n//2 ... 1) — simplest, O(n²) worst case.

    >>> shell_sort_shell([3, 2, 1])
    [1, 2, 3]
    >>> shell_sort_shell([])
    []
    """
    a = list(collection)
    return _shell_sort_with_gaps(a, _gaps_shell(len(a)))


def shell_sort_knuth(collection: list) -> list:
    """Knuth 1973 gaps — O(n^1.5), classic interview answer.

    >>> shell_sort_knuth([3, 2, 1])
    [1, 2, 3]
    >>> shell_sort_knuth([])
    []
    >>> shell_sort_knuth([5, 1, 9, 3, 7])
    [1, 3, 5, 7, 9]
    """
    a = list(collection)
    return _shell_sort_with_gaps(a, _gaps_knuth(len(a)))


def shell_sort_ciura(collection: list) -> list:
    """Ciura 2001 gaps — empirically best known sequence.

    >>> shell_sort_ciura([3, 2, 1])
    [1, 2, 3]
    >>> shell_sort_ciura([])
    []
    >>> shell_sort_ciura([5, 1, 9, 3, 7])
    [1, 3, 5, 7, 9]
    """
    a = list(collection)
    return _shell_sort_with_gaps(a, _gaps_ciura(len(a)))


def shell_sort_tokuda(collection: list) -> list:
    """Tokuda 1992 gaps — closed-form, near-optimal.

    >>> shell_sort_tokuda([3, 2, 1])
    [1, 2, 3]
    >>> shell_sort_tokuda([])
    []
    >>> shell_sort_tokuda([5, 1, 9, 3, 7])
    [1, 3, 5, 7, 9]
    """
    a = list(collection)
    return _shell_sort_with_gaps(a, _gaps_tokuda(len(a)))


def shell_sort_builtin(collection: list) -> list:
    """Python sorted() — Timsort reference.

    >>> shell_sort_builtin([3, 2, 1])
    [1, 2, 3]
    >>> shell_sort_builtin([])
    []
    """
    return sorted(collection)


# ---------------------------------------------------------------------------
# Show gap sequences for a given n
# ---------------------------------------------------------------------------
def show_gaps(n: int = 100) -> None:
    print(f"Gap sequences for n={n}:")
    print(f"  shrink-1.3 : {_gaps_shrink13(n)}")
    print(f"  Shell 1959 : {_gaps_shell(n)}")
    print(f"  Knuth 1973 : {_gaps_knuth(n)}")
    print(f"  Ciura 2001 : {_gaps_ciura(n)}")
    print(f"  Tokuda 1992: {_gaps_tokuda(n)}")


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    variants = [
        ("1. shrink-1.3 (orig)", shell_sort_shrink13),
        ("2. Shell 1959       ", shell_sort_shell),
        ("3. Knuth 1973       ", shell_sort_knuth),
        ("4. Ciura 2001       ", shell_sort_ciura),
        ("5. Tokuda 1992      ", shell_sort_tokuda),
        ("6. sorted()         ", shell_sort_builtin),
    ]

    scenarios = [
        ("random",         lambda n: random.sample(range(n * 2), n)),
        ("sorted",         lambda n: list(range(n))),
        ("reverse sorted", lambda n: list(range(n, 0, -1))),
        ("many dupes",     lambda n: [random.randint(0, 9) for _ in range(n)]),
    ]

    sizes = [1_000, 10_000, 100_000]

    for label, gen in scenarios:
        print(f"\n--- {label} ---")
        for n in sizes:
            data = gen(n)
            print(f"  n={n:,}")
            for name, fn in variants:
                best = float("inf")
                for _ in range(3):
                    t0 = time.perf_counter()
                    result = fn(list(data))
                    best = min(best, time.perf_counter() - t0)
                assert result == sorted(data), f"{name} wrong!"
                print(f"    {name}: {best * 1000:8.2f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\nAll doctests passed.\n")
    show_gaps(100)
    print()
    benchmark()
