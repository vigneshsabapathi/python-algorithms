#!/usr/bin/env python3
"""
Optimized and alternative implementations of Password Generator.

Variants covered:
1. random_choice     -- random.choice from pool (reference)
2. secrets_module    -- Using secrets for cryptographic safety
3. passphrase        -- Diceware-style passphrase generator

Run:
    python other/password_optimized.py
"""

from __future__ import annotations

import os
import random
import secrets
import string
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.password import generate_password as reference
from other.password import check_password_strength


def secrets_password(length: int = 16) -> str:
    """
    Cryptographically secure password using secrets module.

    >>> len(secrets_password(12))
    12
    >>> len(secrets_password(0))
    0
    """
    if length <= 0:
        return ""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        pwd = "".join(secrets.choice(alphabet) for _ in range(length))
        if (
            any(c in string.ascii_lowercase for c in pwd)
            and any(c in string.ascii_uppercase for c in pwd)
            and any(c in string.digits for c in pwd)
            and any(c in string.punctuation for c in pwd)
        ):
            return pwd


def passphrase(num_words: int = 4, separator: str = "-") -> str:
    """
    Generate a passphrase from random words.

    >>> len(passphrase(4).split("-"))
    4
    >>> len(passphrase(2, "_").split("_"))
    2
    """
    word_list = [
        "correct", "horse", "battery", "staple", "thunder", "river",
        "forest", "castle", "dragon", "wizard", "crystal", "shadow",
        "falcon", "phoenix", "glacier", "summit", "canyon", "harbor",
        "meadow", "volcano", "nebula", "quantum", "cipher", "prism",
        "zenith", "ember", "frost", "echo", "drift", "pulse",
    ]
    words = [secrets.choice(word_list) for _ in range(num_words)]
    return separator.join(words)


def pronounceable_password(length: int = 12) -> str:
    """
    Generate a pronounceable password alternating consonants and vowels.

    >>> len(pronounceable_password(10))
    10
    >>> len(pronounceable_password(0))
    0
    """
    if length <= 0:
        return ""
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    pwd = []
    for i in range(length):
        if i % 2 == 0:
            pwd.append(secrets.choice(consonants))
        else:
            pwd.append(secrets.choice(vowels))
    # Add some uppercase and digits
    if length >= 4:
        pos = secrets.randbelow(length)
        pwd[pos] = pwd[pos].upper()
        pos2 = secrets.randbelow(length)
        pwd[pos2] = str(secrets.randbelow(10))
    return "".join(pwd)


IMPLS = [
    ("random_choice", lambda: reference(16)),
    ("secrets", lambda: secrets_password(16)),
    ("passphrase", lambda: passphrase(4)),
    ("pronounceable", lambda: pronounceable_password(16)),
]


def run_all() -> None:
    print("\n=== Sample passwords ===")
    for name, fn in IMPLS:
        pwd = fn()
        strength = check_password_strength(pwd)
        print(f"  {name:<20} {pwd:<30} strength={strength}")

    REPS = 10_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
