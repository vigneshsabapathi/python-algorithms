"""
Password Generator — Generate random secure passwords.

Creates passwords with configurable length, character types, and strength
requirements.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/password.py
"""

from __future__ import annotations

import random
import string


def generate_password(
    length: int = 16,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_digits: bool = True,
    include_special: bool = True,
) -> str:
    """
    Generate a random password with specified character types.

    >>> rng = random.Random(42)
    >>> random.seed(42)
    >>> pwd = generate_password(12)
    >>> len(pwd)
    12
    >>> any(c in string.ascii_uppercase for c in pwd)
    True
    >>> generate_password(0)
    ''
    >>> len(generate_password(8, include_special=False))
    8
    """
    if length <= 0:
        return ""

    chars = ""
    required: list[str] = []

    if include_uppercase:
        chars += string.ascii_uppercase
        required.append(random.choice(string.ascii_uppercase))
    if include_lowercase:
        chars += string.ascii_lowercase
        required.append(random.choice(string.ascii_lowercase))
    if include_digits:
        chars += string.digits
        required.append(random.choice(string.digits))
    if include_special:
        chars += string.punctuation
        required.append(random.choice(string.punctuation))

    if not chars:
        return ""

    # Fill remaining with random chars
    remaining = length - len(required)
    password_chars = required + [random.choice(chars) for _ in range(max(0, remaining))]

    # Shuffle so required chars aren't always at the start
    random.shuffle(password_chars)

    return "".join(password_chars[:length])


def check_password_strength(password: str) -> str:
    """
    Rate password strength as 'weak', 'medium', or 'strong'.

    >>> check_password_strength("")
    'weak'
    >>> check_password_strength("abc")
    'weak'
    >>> check_password_strength("Abcdef1!")
    'strong'
    >>> check_password_strength("Abcdefgh")
    'medium'
    """
    if len(password) < 6:
        return "weak"

    score = 0
    if any(c in string.ascii_uppercase for c in password):
        score += 1
    if any(c in string.ascii_lowercase for c in password):
        score += 1
    if any(c in string.digits for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1
    if len(password) >= 12:
        score += 1

    if score >= 4:
        return "strong"
    elif score >= 2:
        return "medium"
    return "weak"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
