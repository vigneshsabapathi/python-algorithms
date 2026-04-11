"""
SHA-1 (Secure Hash Algorithm 1) -- produces a 160-bit (20-byte) hash value,
typically rendered as a 40-character hexadecimal string.

The algorithm:
1. Pad message to a multiple of 512 bits
2. Split into 512-bit blocks
3. For each block: expand to 80 32-bit words, then 80 rounds of mixing
4. Each round uses one of four functions (Ch, Parity, Maj, Parity)
   with corresponding constants

SHA-1 is deprecated for cryptographic use (collision attacks exist)
but remains useful for checksums and non-security applications.

Reference: https://en.wikipedia.org/wiki/SHA-1
"""

import struct


class SHA1Hash:
    """
    Class to contain the entire pipeline for SHA1 hashing algorithm.

    >>> SHA1Hash(bytes('Allan', 'utf-8')).final_hash()
    '872af2d8ac3d8695387e7c804bf0e02c18df9e6e'

    >>> import hashlib
    >>> msg = b'Hello World'
    >>> SHA1Hash(msg).final_hash() == hashlib.sha1(msg).hexdigest()
    True
    """

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    @staticmethod
    def rotate(n: int, b: int) -> int:
        """
        Left-rotate n by b bits (32-bit).

        >>> SHA1Hash(b'').rotate(12, 2)
        48
        """
        return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

    def padding(self) -> bytes:
        """Pad the input message to a multiple of 512 bits."""
        padding = b"\x80" + b"\x00" * (63 - (len(self.data) + 8) % 64)
        padded_data = self.data + padding + struct.pack(">Q", 8 * len(self.data))
        return padded_data

    def split_blocks(self) -> list[bytes]:
        """Split padded data into 64-byte blocks."""
        return [
            self.padded_data[i : i + 64] for i in range(0, len(self.padded_data), 64)
        ]

    def expand_block(self, block: bytes) -> list[int]:
        """Expand a 64-byte block into 80 32-bit words."""
        w = list(struct.unpack(">16L", block)) + [0] * 64
        for i in range(16, 80):
            w[i] = self.rotate((w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]), 1)
        return w

    def final_hash(self) -> str:
        """
        Process the message and return the SHA-1 hash as hex string.

        >>> SHA1Hash(b'').final_hash()
        'da39a3ee5e6b4b0d3255bfef95601890afd80709'
        """
        self.padded_data = self.padding()
        self.blocks = self.split_blocks()
        for block in self.blocks:
            expanded_block = self.expand_block(block)
            a, b, c, d, e = self.h
            for i in range(80):
                if 0 <= i < 20:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i < 40:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                else:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                a, b, c, d, e = (
                    (self.rotate(a, 5) + f + e + k + expanded_block[i]) & 0xFFFFFFFF,
                    a,
                    self.rotate(b, 30),
                    c,
                    d,
                )
            self.h = (
                (self.h[0] + a) & 0xFFFFFFFF,
                (self.h[1] + b) & 0xFFFFFFFF,
                (self.h[2] + c) & 0xFFFFFFFF,
                (self.h[3] + d) & 0xFFFFFFFF,
                (self.h[4] + e) & 0xFFFFFFFF,
            )
        return ("{:08x}" * 5).format(*self.h)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
