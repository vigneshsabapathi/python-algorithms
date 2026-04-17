"""
Simple Keyword Cipher
======================
A substitution cipher that maps each letter of the alphabet to a letter in a
shifted alphabet built from a keyword:
  - The keyword letters (deduped) come first.
  - Remaining alphabet letters follow in order.

https://en.wikipedia.org/wiki/Keyword_cipher
"""


def remove_duplicates(key: str) -> str:
    """
    Remove duplicate alphabetic characters while preserving spaces.

    >>> remove_duplicates('Hello World!!')
    'Helo Wrd'
    """
    key_no_dups = ""
    for ch in key:
        if ch == " " or (ch not in key_no_dups and ch.isalpha()):
            key_no_dups += ch
    return key_no_dups


def create_cipher_map(key: str) -> dict[str, str]:
    """
    Build a substitution mapping for the 26 uppercase letters.

    >>> create_cipher_map('Goodbye!!')['A']
    'G'
    >>> create_cipher_map('Goodbye!!')['H']
    'C'
    """
    alphabet = [chr(i + 65) for i in range(26)]
    key = remove_duplicates(key.upper())
    offset = len(key)
    cipher_alphabet = {alphabet[i]: char for i, char in enumerate(key)}
    for i in range(len(cipher_alphabet), 26):
        char = alphabet[i - offset]
        while char in key:
            offset -= 1
            char = alphabet[i - offset]
        cipher_alphabet[alphabet[i]] = char
    return cipher_alphabet


def encipher(message: str, cipher_map: dict[str, str]) -> str:
    """
    Encipher *message* using *cipher_map*.

    >>> encipher('Hello World!!', create_cipher_map('Goodbye!!'))
    'CYJJM VMQJB!!'
    """
    return "".join(cipher_map.get(ch, ch) for ch in message.upper())


def decipher(message: str, cipher_map: dict[str, str]) -> str:
    """
    Decipher *message* by reversing *cipher_map*.

    >>> cipher_map = create_cipher_map('Goodbye!!')
    >>> decipher(encipher('Hello World!!', cipher_map), cipher_map)
    'HELLO WORLD!!'
    """
    rev = {v: k for k, v in cipher_map.items()}
    return "".join(rev.get(ch, ch) for ch in message.upper())


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    cm = create_cipher_map("Goodbye!!")
    enc = encipher("Hello World!!", cm)
    print(f"Enciphered: {enc}")
    print(f"Deciphered: {decipher(enc, cm)}")
