"""
SDBM hash -- created for the sdbm (public-domain reimplementation of ndbm)
database library. Found to scramble bits well, causing better key distribution
and fewer splits.

The algorithm:
    hash(i) = hash(i-1) * 65599 + str[i]

The faster equivalent used in gawk:
    hash(i) = str[i] + (hash(i-1) << 6) + (hash(i-1) << 16) - hash(i-1)

The magic constant 65599 was picked experimentally and happens to be prime.

source: http://www.cse.yorku.ca/~oz/hash.html
"""


def sdbm(plain_text: str) -> int:
    """
    SDBM hash function -- good for general hashing with nice bit distribution.

    >>> sdbm('Algorithms')
    1462174910723540325254304520539387479031000036

    >>> sdbm('scramble bits')
    730247649148944819640658295400555317318720608290373040936089

    >>> sdbm('')
    0

    >>> sdbm('a')
    97
    """
    hash_value = 0
    for plain_chr in plain_text:
        hash_value = (
            ord(plain_chr) + (hash_value << 6) + (hash_value << 16) - hash_value
        )
    return hash_value


if __name__ == "__main__":
    import doctest

    doctest.testmod()
