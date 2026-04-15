#!/usr/bin/env python3
"""
Optimized and alternative implementations of FizzBuzz.

Four variants:
  conditional     — classic if/elif chain (reference)
  dict_lookup     — dictionary-based divisibility lookup
  list_comprehend — one-liner list comprehension
  no_modulo       — counter-based, avoids modulo operator

Run:
    python dynamic_programming/fizz_buzz_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.fizz_buzz import fizz_buzz as reference


# ---------------------------------------------------------------------------
# Variant 1 — conditional (same as reference)
# ---------------------------------------------------------------------------

def conditional(start: int, end: int) -> str:
    """
    >>> conditional(1, 7)
    '1 2 Fizz 4 Buzz Fizz 7 '
    """
    return reference(start, end)


# ---------------------------------------------------------------------------
# Variant 2 — dict_lookup: Dictionary-based
# ---------------------------------------------------------------------------

def dict_lookup(start: int, end: int) -> str:
    """
    >>> dict_lookup(1, 15)
    '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz '
    """
    out = []
    for n in range(start, end + 1):
        s = ""
        if n % 3 == 0:
            s += "Fizz"
        if n % 5 == 0:
            s += "Buzz"
        out.append(s or str(n))
    return " ".join(out) + " "


# ---------------------------------------------------------------------------
# Variant 3 — list_comprehend: One-liner
# ---------------------------------------------------------------------------

def list_comprehend(start: int, end: int) -> str:
    """
    >>> list_comprehend(1, 7)
    '1 2 Fizz 4 Buzz Fizz 7 '
    """
    return " ".join(
        "FizzBuzz" if n % 15 == 0 else
        "Fizz" if n % 3 == 0 else
        "Buzz" if n % 5 == 0 else
        str(n)
        for n in range(start, end + 1)
    ) + " "


# ---------------------------------------------------------------------------
# Variant 4 — no_modulo: Counter-based (avoids modulo)
# ---------------------------------------------------------------------------

def no_modulo(start: int, end: int) -> str:
    """
    Uses counters instead of modulo — useful in constrained environments.

    >>> no_modulo(1, 15)
    '1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz '
    """
    out = []
    fizz_counter = start % 3 if start % 3 != 0 else 3
    buzz_counter = start % 5 if start % 5 != 0 else 5
    for n in range(start, end + 1):
        s = ""
        if fizz_counter == 3:
            s += "Fizz"
            fizz_counter = 0
        if buzz_counter == 5:
            s += "Buzz"
            buzz_counter = 0
        if not s:
            s = str(n)
        out.append(s)
        fizz_counter += 1
        buzz_counter += 1
    return " ".join(out) + " "


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

IMPLS = [
    ("conditional", conditional),
    ("dict_lookup", dict_lookup),
    ("list_comprehend", list_comprehend),
    ("no_modulo", no_modulo),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for start, end in [(1, 7), (1, 15), (1, 30), (10, 20)]:
        ref = reference(start, end)
        for name, fn in IMPLS:
            result = fn(start, end)
            ok = result == ref
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}({start}, {end}) len={len(result)}")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 50_000
    print(f"\n=== Benchmark (1 to 100): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(1, 100), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
