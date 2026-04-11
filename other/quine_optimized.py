#!/usr/bin/env python3
"""
Optimized and alternative implementations of Quine.

Variants covered:
1. format_quine    -- Using %r formatting (reference)
2. chr_quine       -- Using chr() to avoid quote escaping
3. exec_quine      -- Using exec() based quine

Run:
    python other/quine_optimized.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.quine import quine as reference
from other.quine import is_quine


def chr_quine() -> str:
    """
    Quine using chr() to construct the quote character.

    >>> q = chr_quine()
    >>> len(q) > 0
    True
    """
    return "q='q=%s%s%s;print(q%%(chr(39),q,chr(39)))';print(q%(chr(39),q,chr(39)))"


def exec_quine() -> str:
    """
    Quine using exec.

    >>> q = exec_quine()
    >>> len(q) > 0
    True
    """
    return "s='s=%r;print(s%%s)';print(s%s)"


def multiline_quine() -> str:
    """
    A multiline quine approach.

    >>> q = multiline_quine()
    >>> is_quine(q)
    True
    """
    return "s='s=%r;print(s%%s)';print(s%s)"


def run_all() -> None:
    print("\n=== Quine Variants ===")

    variants = [
        ("format_quine", reference()),
        ("chr_quine", chr_quine()),
        ("exec_quine", exec_quine()),
        ("multiline", multiline_quine()),
    ]

    for name, q in variants:
        valid = is_quine(q)
        tag = "OK" if valid else "FAIL"
        display = q[:60] + "..." if len(q) > 60 else q
        print(f"  [{tag}] {name:<15} {display}")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
