"""
Quine — A program that prints its own source code.

A quine is a non-empty program that takes no input and produces its own
source code as output. This module implements the quine concept along with
a validator.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/quine.py
"""

from __future__ import annotations


def quine() -> str:
    """
    Return a string that is a valid Python quine (prints itself).

    >>> q = quine()
    >>> len(q) > 0
    True
    >>> 'exec' in q or 'print' in q or 'chr' in q
    True
    """
    # Classic two-part quine: data + code that prints data + code
    source = 's=%r;print(s%%s)'
    return source % source


def is_quine(program: str) -> bool:
    """
    Check if a given Python program is a quine (its output equals its source).

    >>> is_quine("s='s=%r;print(s%%s)';print(s%s)")
    True
    >>> is_quine("print('hello')")
    False
    >>> is_quine("")
    False
    """
    if not program:
        return False

    import io
    import contextlib

    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(program)  # noqa: S102
    except Exception:
        return False

    return output.getvalue().strip() == program.strip()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
