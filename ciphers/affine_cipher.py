"""
Affine Cipher — a monoalphabetic substitution cipher using the formula:
    E(x) = (a*x + b) mod m
    D(y) = a_inv * (y - b) mod m

where m = 94 (printable ASCII symbols), and gcd(a, m) == 1.

References:
    https://en.wikipedia.org/wiki/Affine_cipher
"""

import random
from math import gcd

SYMBOLS = (
    r""" !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`"""
    r"""abcdefghijklmnopqrstuvwxyz{|}~"""
)


def _find_mod_inverse(a: int, m: int) -> int:
    """
    Find the modular multiplicative inverse of a mod m using extended Euclidean.

    >>> _find_mod_inverse(7, 26)
    15
    >>> _find_mod_inverse(3, 94)
    63
    """
    if gcd(a, m) != 1:
        raise ValueError(f"mod inverse of {a!r} and {m!r} does not exist")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def check_keys(key_a: int, key_b: int, mode: str) -> None:
    """
    Validate affine cipher keys.

    >>> check_keys(47, 12, "encrypt")
    >>> check_keys(1, 12, "encrypt")
    Traceback (most recent call last):
        ...
    ValueError: Key A=1 makes the affine cipher a simple Caesar cipher (weak).
    """
    if mode == "encrypt":
        if key_a == 1:
            raise ValueError(
                "Key A=1 makes the affine cipher a simple Caesar cipher (weak)."
            )
        if key_b == 0:
            raise ValueError(
                "Key B=0 makes the affine cipher a simple Caesar cipher (weak)."
            )
    if key_a < 0 or key_b < 0 or key_b > len(SYMBOLS) - 1:
        raise ValueError(
            f"Key A must be > 0 and Key B must be in [0, {len(SYMBOLS) - 1}]."
        )
    if gcd(key_a, len(SYMBOLS)) != 1:
        raise ValueError(
            f"Key A={key_a} and symbol set size {len(SYMBOLS)} are not coprime."
        )


def encrypt_message(key: int, message: str) -> str:
    """
    Encrypt a message with the affine cipher using a composite key.

    The composite key encodes both a and b: key = a * len(SYMBOLS) + b.

    >>> encrypt_message(4545, 'The affine cipher is a type of monoalphabetic substitution cipher.')
    'VL}p MM{I}p~{HL}Gp{vp pFsH}pxMpyxIx JHL O}F{~pvuOvF{FuF{xIp~{HL}Gi'
    """
    key_a, key_b = divmod(key, len(SYMBOLS))
    check_keys(key_a, key_b, "encrypt")
    cipher_text = ""
    for symbol in message:
        if symbol in SYMBOLS:
            sym_index = SYMBOLS.find(symbol)
            cipher_text += SYMBOLS[(sym_index * key_a + key_b) % len(SYMBOLS)]
        else:
            cipher_text += symbol
    return cipher_text


def decrypt_message(key: int, message: str) -> str:
    """
    Decrypt an affine-cipher message.

    >>> decrypt_message(4545, 'VL}p MM{I}p~{HL}Gp{vp pFsH}pxMpyxIx JHL O}F{~pvuOvF{FuF{xIp~{HL}Gi')
    'The affine cipher is a type of monoalphabetic substitution cipher.'
    """
    key_a, key_b = divmod(key, len(SYMBOLS))
    check_keys(key_a, key_b, "decrypt")
    plain_text = ""
    mod_inverse_of_key_a = _find_mod_inverse(key_a, len(SYMBOLS))
    for symbol in message:
        if symbol in SYMBOLS:
            sym_index = SYMBOLS.find(symbol)
            plain_text += SYMBOLS[(sym_index - key_b) * mod_inverse_of_key_a % len(SYMBOLS)]
        else:
            plain_text += symbol
    return plain_text


def get_random_key() -> int:
    """
    Generate a random valid affine cipher key.

    >>> key = get_random_key()
    >>> key_a, key_b = divmod(key, len(SYMBOLS))
    >>> gcd(key_a, len(SYMBOLS)) == 1
    True
    """
    while True:
        key_a = random.randint(2, len(SYMBOLS))
        key_b = random.randint(2, len(SYMBOLS))
        if gcd(key_a, len(SYMBOLS)) == 1 and key_b % len(SYMBOLS) != 0:
            return key_a * len(SYMBOLS) + key_b


if __name__ == "__main__":
    import doctest
    doctest.testmod()
