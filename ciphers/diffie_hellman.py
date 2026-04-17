"""
Diffie-Hellman Key Exchange using RFC 3526 MODP Groups.

Implements the standard DH protocol with 2048-bit (Group 14) prime by default.
Public key validation follows NIST SP800-56A Rev3 §5.6.2.3.

Both parties independently compute the same shared secret:
    shared = pow(other_public, private, prime)

References:
    https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
    https://www.rfc-editor.org/rfc/rfc3526
"""

from __future__ import annotations

import hashlib
import os


# RFC 3526 Group 14 — 2048-bit MODP prime (hex, generator g=2)
MODP_GROUPS: dict[int, dict[str, int]] = {
    14: {
        "prime": int(
            "FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1"
            "29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD"
            "EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245"
            "E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED"
            "EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D"
            "C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F"
            "83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D"
            "670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B"
            "E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9"
            "DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510"
            "15728E5A 8AACAA68 FFFFFFFF FFFFFFFF".replace(" ", ""),
            16,
        ),
        "generator": 2,
    },
}


class DiffieHellman:
    """
    Diffie-Hellman key exchange using RFC 3526 MODP groups.

    >>> dh = DiffieHellman()
    >>> pub = dh.get_public_key()
    >>> isinstance(pub, bytes)
    True
    """

    def __init__(self, group: int = 14) -> None:
        self.prime = MODP_GROUPS[group]["prime"]
        self.generator = MODP_GROUPS[group]["generator"]
        self.__private_key = int.from_bytes(os.urandom(32), "big")

    def get_private_key(self) -> str:
        """Return private key as hex string."""
        return hex(self.__private_key)

    def get_public_key(self) -> bytes:
        """Compute and return public key as bytes."""
        public_key = pow(self.generator, self.__private_key, self.prime)
        return public_key.to_bytes(256, "big")

    def check_public_key(self, other_key_bytes: bytes) -> bool:
        """
        Validate a received public key per NIST SP800-56A.

        Key k is valid if: 2 <= k <= prime-2 AND k^((prime-1)//2) mod prime == 1
        """
        other_key = int.from_bytes(other_key_bytes, "big")
        if not (2 <= other_key <= self.prime - 2):
            return False
        if pow(other_key, (self.prime - 1) // 2, self.prime) != 1:
            return False
        return True

    def generate_shared_key(self, other_key_bytes: bytes) -> bytes:
        """
        Compute the shared secret and return its SHA-256 hash as bytes.

        >>> dh_a = DiffieHellman()
        >>> dh_b = DiffieHellman()
        >>> pub_a = dh_a.get_public_key()
        >>> pub_b = dh_b.get_public_key()
        >>> dh_a.generate_shared_key(pub_b) == dh_b.generate_shared_key(pub_a)
        True
        """
        other_key = int.from_bytes(other_key_bytes, "big")
        shared = pow(other_key, self.__private_key, self.prime)
        return hashlib.sha256(shared.to_bytes(256, "big")).digest()

    @staticmethod
    def generate_shared_key_static(
        my_private_key_str: str, other_public_key_bytes: bytes, group: int = 14
    ) -> bytes:
        """
        Static helper: compute shared key given private key (hex str) and
        the other party's public key bytes.

        >>> dh = DiffieHellman()
        >>> priv = dh.get_private_key()
        >>> pub = dh.get_public_key()
        >>> sk = DiffieHellman.generate_shared_key_static(priv, pub)
        >>> isinstance(sk, bytes) and len(sk) == 32
        True
        """
        prime = MODP_GROUPS[group]["prime"]
        my_private_key = int(my_private_key_str, 16)
        other_key = int.from_bytes(other_public_key_bytes, "big")
        shared = pow(other_key, my_private_key, prime)
        return hashlib.sha256(shared.to_bytes(256, "big")).digest()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
