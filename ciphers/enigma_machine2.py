"""
Enigma Machine Emulator.

Emulates the WWII Enigma machine with 3 configurable rotors, a reflector, and
an optional plugboard. Encryption and decryption use the same operation
(the reflector makes it self-reciprocal).

Non-alphabetic characters pass through unchanged. All input is uppercased.

References:
    https://en.wikipedia.org/wiki/Enigma_machine
    https://youtu.be/QwQVMqfoB2E
"""

from __future__ import annotations

RotorPositionT = tuple[int, int, int]
RotorSelectionT = tuple[str, str, str]

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Default rotors
rotor1 = "EGZWVONAHDCLFQMSIPJBYUKXTR"
rotor2 = "FOBHMDKEXQNRAULPGSJVTYICZW"
rotor3 = "ZJXESIUQLHAVRMDOYGTNFWPBKC"

# Reflector (static rotor — symmetric pairings)
reflector = {
    "A": "N", "N": "A", "B": "O", "O": "B", "C": "P", "P": "C",
    "D": "Q", "Q": "D", "E": "R", "R": "E", "F": "S", "S": "F",
    "G": "T", "T": "G", "H": "U", "U": "H", "I": "V", "V": "I",
    "J": "W", "W": "J", "K": "X", "X": "K", "L": "Y", "Y": "L",
    "M": "Z", "Z": "M",
}

# Extra rotors
rotor4 = "RMDJXFUWGISLHVTCQNKYPBEZOA"
rotor5 = "SGLCPQWZHKXAREONTFBVIYJUDM"
rotor6 = "HVSICLTYKQUBXDWAJZOMFGPREN"
rotor7 = "RZWQHFMVDBKICJLNTUXAGYPSOE"
rotor8 = "LFKIJODBEGAMQPXVUHYSTCZRWN"
rotor9 = "KOAEGVDHXPQZMLFTYWJNBRCIUS"


def _plugboard(pbstring: str) -> dict[str, str]:
    """
    Parse a plugboard string into a swap dictionary.

    >>> _plugboard('PICTURES')
    {'P': 'I', 'I': 'P', 'C': 'T', 'T': 'C', 'U': 'R', 'R': 'U', 'E': 'S', 'S': 'E'}
    >>> _plugboard('POLAND')
    {'P': 'O', 'O': 'P', 'L': 'A', 'A': 'L', 'N': 'D', 'D': 'N'}
    >>> _plugboard('')
    {}
    """
    if not isinstance(pbstring, str):
        raise TypeError(f"Plugboard setting isn't type string ({type(pbstring)})")
    if len(pbstring) % 2 != 0:
        raise Exception(f"Odd number of symbols ({len(pbstring)})")
    if pbstring == "":
        return {}
    pbstring = pbstring.replace(" ", "")
    seen: set[str] = set()
    for ch in pbstring:
        if ch not in abc:
            raise Exception(f"'{ch}' not in list of symbols")
        if ch in seen:
            raise Exception(f"Duplicate symbol ({ch})")
        seen.add(ch)
    pb: dict[str, str] = {}
    for j in range(0, len(pbstring) - 1, 2):
        pb[pbstring[j]] = pbstring[j + 1]
        pb[pbstring[j + 1]] = pbstring[j]
    return pb


def _validator(
    rotpos: RotorPositionT, rotsel: RotorSelectionT, pb: str
) -> tuple[RotorPositionT, RotorSelectionT, dict[str, str]]:
    """
    Validate rotor positions, rotor selection uniqueness, and plugboard string.

    >>> _validator((1,1,1), (rotor1, rotor2, rotor3), 'POLAND')
    ((1, 1, 1), ('EGZWVONAHDCLFQMSIPJBYUKXTR', 'FOBHMDKEXQNRAULPGSJVTYICZW', \
'ZJXESIUQLHAVRMDOYGTNFWPBKC'), \
{'P': 'O', 'O': 'P', 'L': 'A', 'A': 'L', 'N': 'D', 'D': 'N'})
    """
    if (unique := len(set(rotsel))) < 3:
        raise Exception(f"Please use 3 unique rotors (not {unique})")
    rp1, rp2, rp3 = rotpos
    if not 0 < rp1 <= len(abc):
        raise ValueError(f"First rotor position is not within range of 1..26 ({rp1}")
    if not 0 < rp2 <= len(abc):
        raise ValueError(f"Second rotor position is not within range of 1..26 ({rp2})")
    if not 0 < rp3 <= len(abc):
        raise ValueError(f"Third rotor position is not within range of 1..26 ({rp3})")
    pbdict = _plugboard(pb)
    return rotpos, rotsel, pbdict


def enigma(
    text: str,
    rotor_position: RotorPositionT,
    rotor_selection: RotorSelectionT = (rotor1, rotor2, rotor3),
    plugb: str = "",
) -> str:
    """
    Encrypt or decrypt text using the Enigma machine emulator.

    Input is converted to uppercase; non-letter characters pass through unchanged.
    Encryption and decryption are the same operation.

    >>> enigma('Hello World!', (1, 2, 1), plugb='pictures')
    'KORYH JUHHI!'
    >>> enigma('KORYH, juhhi!', (1, 2, 1), plugb='pictures')
    'HELLO, WORLD!'
    >>> enigma('hello world!', (1, 1, 1), plugb='pictures')
    'FPNCZ QWOBU!'
    >>> enigma('FPNCZ QWOBU', (1, 1, 1), plugb='pictures')
    'HELLO WORLD'
    """
    text = text.upper()
    rotor_position, rotor_selection, plugboard = _validator(
        rotor_position, rotor_selection, plugb.upper()
    )

    rotorpos1, rotorpos2, rotorpos3 = rotor_position
    r1, r2, r3 = rotor_selection
    rotorpos1 -= 1
    rotorpos2 -= 1
    rotorpos3 -= 1

    result = []

    for symbol in text:
        if symbol in abc:
            if symbol in plugboard:
                symbol = plugboard[symbol]

            symbol = r1[(abc.index(symbol) + rotorpos1) % len(abc)]
            symbol = r2[(abc.index(symbol) + rotorpos2) % len(abc)]
            symbol = r3[(abc.index(symbol) + rotorpos3) % len(abc)]

            symbol = reflector[symbol]

            symbol = abc[r3.index(symbol) - rotorpos3]
            symbol = abc[r2.index(symbol) - rotorpos2]
            symbol = abc[r1.index(symbol) - rotorpos1]

            if symbol in plugboard:
                symbol = plugboard[symbol]

            rotorpos1 += 1
            if rotorpos1 >= len(abc):
                rotorpos1 = 0
                rotorpos2 += 1
            if rotorpos2 >= len(abc):
                rotorpos2 = 0
                rotorpos3 += 1
            if rotorpos3 >= len(abc):
                rotorpos3 = 0

        result.append(symbol)

    return "".join(result)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
