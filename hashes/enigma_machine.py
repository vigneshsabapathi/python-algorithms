"""
Enigma Machine -- a simplified simulation of the famous WWII cipher machine.

The Enigma machine uses a series of rotors (gears) and a reflector to
substitute each input character. After each character is encrypted, the
rotors advance (like an odometer), changing the substitution for the
next character. This makes it a polyalphabetic cipher.

This implementation uses 3 gears + 1 reflector operating on printable
ASCII characters (codes 32-125, 94 characters).

source: https://github.com/TheAlgorithms/Python/blob/master/hashes/enigma_machine.py
"""

from __future__ import annotations


def _make_default_config() -> dict:
    """Create default Enigma machine configuration."""
    alphabets = [chr(i) for i in range(32, 126)]
    n = len(alphabets)
    return {
        "alphabets": alphabets,
        "gear_one": list(range(n)),
        "gear_two": list(range(n)),
        "gear_three": list(range(n)),
        "reflector": list(reversed(range(n))),
        "gear_one_pos": 0,
        "gear_two_pos": 0,
        "gear_three_pos": 0,
    }


def _rotator(config: dict) -> None:
    """Advance the rotors (odometer-style)."""
    n = len(config["alphabets"])
    g1 = config["gear_one"]
    g2 = config["gear_two"]
    g3 = config["gear_three"]

    i = g1[0]
    g1.append(i)
    del g1[0]
    config["gear_one_pos"] += 1

    if config["gear_one_pos"] % n == 0:
        i = g2[0]
        g2.append(i)
        del g2[0]
        config["gear_two_pos"] += 1

        if config["gear_two_pos"] % n == 0:
            i = g3[0]
            g3.append(i)
            del g3[0]
            config["gear_three_pos"] += 1


def _engine(input_char: str, config: dict) -> str:
    """Encrypt a single character through the Enigma machine."""
    alphabets = config["alphabets"]
    g1 = config["gear_one"]
    g2 = config["gear_two"]
    g3 = config["gear_three"]
    ref = config["reflector"]

    # Forward through gears
    target = alphabets.index(input_char)
    target = g1[target]
    target = g2[target]
    target = g3[target]

    # Reflector
    target = ref[target]

    # Backward through gears
    target = g3.index(target)
    target = g2.index(target)
    target = g1.index(target)

    _rotator(config)
    return alphabets[target]


def enigma_encrypt(message: str, token: int = 0) -> str:
    """
    Encrypt a message using the Enigma machine.

    The token acts as an initial rotor position offset.

    >>> enigma_encrypt('Hello', 0)
    'U6-+&'

    >>> enigma_encrypt('a', 0)
    '<'

    >>> enigma_encrypt('', 0)
    ''

    >>> msg = 'Hello World'
    >>> enc = enigma_encrypt(msg, 42)
    >>> dec = enigma_encrypt(enc, 42)
    >>> dec == msg
    True
    """
    config = _make_default_config()
    # Apply token offset
    for _ in range(token):
        _rotator(config)

    result = []
    for char in message:
        result.append(_engine(char, config))
    return "".join(result)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
