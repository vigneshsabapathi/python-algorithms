"""
ELF hash (Executable and Linkable Format hash) -- a variant of the PJW
hash function, widely used in UNIX ELF object files for symbol table
hashing.

The algorithm shifts the hash left by 4 bits, adds the character value,
then checks the high nibble. If set, it XORs the high nibble back into
the lower bits and clears the high nibble.

This prevents the hash from growing unboundedly while mixing upper bits
back into the result, providing good distribution for symbol names.
"""


def elf_hash(data: str) -> int:
    """
    Implementation of ElfHash Algorithm, a variant of PJW hash function.

    >>> elf_hash('lorem ipsum')
    253956621

    >>> elf_hash('')
    0

    >>> elf_hash('a')
    97

    >>> elf_hash('Hello World')
    18131988
    """
    hash_ = x = 0
    for letter in data:
        hash_ = (hash_ << 4) + ord(letter)
        x = hash_ & 0xF0000000
        if x != 0:
            hash_ ^= x >> 24
        hash_ &= ~x
    return hash_


if __name__ == "__main__":
    import doctest

    doctest.testmod()
