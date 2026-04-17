"""
Caesar Cipher — a substitution cipher that shifts each letter by a fixed key.

Named after Julius Caesar, who used a shift of 3. Characters not in the
alphabet are preserved unchanged. Supports custom alphabets.

References:
    https://en.wikipedia.org/wiki/Caesar_cipher
"""

from __future__ import annotations

from string import ascii_letters


def encrypt(input_string: str, key: int, alphabet: str | None = None) -> str:
    """
    Encrypt a string by shifting each letter forward by `key` positions.

    >>> encrypt('The quick brown fox jumps over the lazy dog', 8)
    'bpm yCqks jzwEv nwF rCuxA wDmz Bpm tiHG lwo'
    >>> encrypt('A very large key', 8000)
    's nWjq dSjYW cWq'
    >>> encrypt('a lowercase alphabet', 5, 'abcdefghijklmnopqrstuvwxyz')
    'f qtbjwhfxj fqumfgjy'
    """
    alpha = alphabet or ascii_letters
    result = ""
    for character in input_string:
        if character not in alpha:
            result += character
        else:
            new_key = (alpha.index(character) + key) % len(alpha)
            result += alpha[new_key]
    return result


def decrypt(input_string: str, key: int, alphabet: str | None = None) -> str:
    """
    Decrypt a Caesar-encrypted string by shifting back by `key` positions.

    >>> decrypt('bpm yCqks jzwEv nwF rCuxA wDmz Bpm tiHG lwo', 8)
    'The quick brown fox jumps over the lazy dog'
    >>> decrypt('s nWjq dSjYW cWq', 8000)
    'A very large key'
    >>> decrypt('f qtbjwhfxj fqumfgjy', 5, 'abcdefghijklmnopqrstuvwxyz')
    'a lowercase alphabet'
    """
    return encrypt(input_string, -key, alphabet)


def brute_force(input_string: str, alphabet: str | None = None) -> dict[int, str]:
    """
    Return all possible decryptions as {key: decrypted_string}.

    >>> brute_force("jFyuMy xIH'N vLONy zILwy Gy!")[20]
    "Please don't brute force me!"
    >>> brute_force(1)
    Traceback (most recent call last):
    TypeError: 'int' object is not iterable
    """
    alpha = alphabet or ascii_letters
    brute_force_data = {}
    for key in range(1, len(alpha) + 1):
        brute_force_data[key] = decrypt(input_string, key, alpha)
    return brute_force_data


if __name__ == "__main__":
    import doctest
    doctest.testmod()
