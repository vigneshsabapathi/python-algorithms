"""
SHA-256 (Secure Hash Algorithm 256-bit) -- part of the SHA-2 family.
Produces a 256-bit (32-byte) hash value, rendered as a 64-character hex string.

The algorithm:
1. Pad message to a multiple of 512 bits
2. Split into 512-bit (64-byte) blocks
3. For each block: expand 16 words to 64 words using sigma functions
4. Run 64 rounds of compression using Ch, Maj, Sigma functions
5. Add compressed values to running hash state

SHA-256 is widely used in TLS, Bitcoin, and digital signatures.

References:
  https://en.wikipedia.org/wiki/SHA-2
  https://qvault.io/cryptography/how-sha-2-works-step-by-step-sha-256/
"""

import struct


class SHA256:
    """
    SHA-256 hash implementation.

    >>> SHA256(b'Python').hash
    '18885f27b5af9012df19e496460f9294d5ab76128824c6f993787004f6d9a7db'

    >>> SHA256(b'hello world').hash
    'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'

    >>> SHA256(b'').hash
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    """

    def __init__(self, data: bytes) -> None:
        self.data = data
        self.hashes = [
            0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
            0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
        ]
        self.round_constants = [
            0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
            0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
            0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3,
            0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
            0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC,
            0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
            0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7,
            0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
            0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13,
            0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
            0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3,
            0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
            0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5,
            0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
            0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208,
            0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2,
        ]
        self.preprocessed_data = self.preprocessing(self.data)
        self.final_hash()

    @staticmethod
    def preprocessing(data: bytes) -> bytes:
        """Pad data to a multiple of 512 bits."""
        padding = b"\x80" + (b"\x00" * (63 - (len(data) + 8) % 64))
        big_endian_integer = struct.pack(">Q", (len(data) * 8))
        return data + padding + big_endian_integer

    def final_hash(self) -> None:
        """Process all blocks and compute the final hash."""
        self.blocks = [
            self.preprocessed_data[x : x + 64]
            for x in range(0, len(self.preprocessed_data), 64)
        ]

        for block in self.blocks:
            words = list(struct.unpack(">16L", block))
            words += [0] * 48

            a, b, c, d, e, f, g, h = self.hashes

            for index in range(64):
                if index > 15:
                    s0 = (
                        self.ror(words[index - 15], 7)
                        ^ self.ror(words[index - 15], 18)
                        ^ (words[index - 15] >> 3)
                    )
                    s1 = (
                        self.ror(words[index - 2], 17)
                        ^ self.ror(words[index - 2], 19)
                        ^ (words[index - 2] >> 10)
                    )
                    words[index] = (
                        words[index - 16] + s0 + words[index - 7] + s1
                    ) % 0x100000000

                s1 = self.ror(e, 6) ^ self.ror(e, 11) ^ self.ror(e, 25)
                ch = (e & f) ^ ((~e & 0xFFFFFFFF) & g)
                temp1 = (
                    h + s1 + ch + self.round_constants[index] + words[index]
                ) % 0x100000000
                s0 = self.ror(a, 2) ^ self.ror(a, 13) ^ self.ror(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (s0 + maj) % 0x100000000

                h, g, f, e, d, c, b, a = (
                    g, f, e,
                    (d + temp1) % 0x100000000,
                    c, b, a,
                    (temp1 + temp2) % 0x100000000,
                )

            mutated = [a, b, c, d, e, f, g, h]
            self.hashes = [
                (element + mutated[i]) % 0x100000000
                for i, element in enumerate(self.hashes)
            ]

        self.hash = "".join(hex(v)[2:].zfill(8) for v in self.hashes)

    def ror(self, value: int, rotations: int) -> int:
        """Right-rotate value by rotations bits (32-bit)."""
        return 0xFFFFFFFF & (value << (32 - rotations)) | (value >> rotations)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
