"""
DJB2 hash algorithm by Dan Bernstein, first reported in comp.lang.c.

The algorithm uses two magic constants:
  - 33 (the multiplier): works better than many other constants, prime or not
  - 5381 (the initial value): an odd prime with nice binary pattern 001/010/100/000/101

The formula: hash(i) = hash(i-1) * 33 + str[i]
Which is equivalent to: hash(i) = (hash(i-1) << 5) + hash(i-1) + str[i]

An alternate XOR version uses:
  hash(i) = hash(i-1) * 33 ^ str[i]

source: http://www.cse.yorku.ca/~oz/hash.html
"""


def djb2(s: str) -> int:
    """
    Implementation of djb2 hash algorithm that
    is popular because of its magic constants.

    >>> djb2('Algorithms')
    3782405311

    >>> djb2('scramble bits')
    1609059040

    >>> djb2('')
    5381

    >>> djb2('a')
    177670
    """
    hash_value = 5381
    for x in s:
        hash_value = ((hash_value << 5) + hash_value) + ord(x)
    return hash_value & 0xFFFFFFFF


if __name__ == "__main__":
    import doctest

    doctest.testmod()
