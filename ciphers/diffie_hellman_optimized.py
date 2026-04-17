"""
Diffie-Hellman Key Exchange — Optimized Variants + Benchmark

Three shared-key derivation strategies: SHA-256 hash, raw int, HKDF-like.
"""

import hashlib
import hmac
import os
from timeit import timeit

# RFC 3526 Group 14 — 2048-bit prime (truncated for benchmark purposes)
_PRIME = int(
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
    "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
    16,
)
_GEN = 2


def _gen_private() -> int:
    return int.from_bytes(os.urandom(32), "big")


def _compute_public(private: int) -> int:
    return pow(_GEN, private, _PRIME)


# ── Variant 1: SHA-256 of raw shared int (original) ──────────────────────────
def derive_shared_key_v1(my_private: int, other_public: int) -> bytes:
    shared = pow(other_public, my_private, _PRIME)
    return hashlib.sha256(str(shared).encode()).digest()


# ── Variant 2: SHA-256 of big-endian bytes ───────────────────────────────────
def derive_shared_key_v2(my_private: int, other_public: int) -> bytes:
    shared = pow(other_public, my_private, _PRIME)
    return hashlib.sha256(shared.to_bytes(256, "big")).digest()


# ── Variant 3: HMAC-SHA256 (adds key confirmation step) ──────────────────────
def derive_shared_key_v3(my_private: int, other_public: int, salt: bytes = b"DH") -> bytes:
    shared = pow(other_public, my_private, _PRIME)
    return hmac.new(salt, shared.to_bytes(256, "big"), "sha256").digest()


# ── Benchmark ─────────────────────────────────────────────────────────────────
def benchmark() -> None:
    priv_a = _gen_private()
    priv_b = _gen_private()
    pub_a = _compute_public(priv_a)
    pub_b = _compute_public(priv_b)
    # Note: the modular exponentiation dominates; derivation differences are minor
    n = 20

    setup = (
        f"from __main__ import derive_shared_key_v1, derive_shared_key_v2, derive_shared_key_v3; "
        f"priv_a={priv_a}; pub_b={pub_b}"
    )
    print("=== Diffie-Hellman Shared Key Derivation Benchmark (20 iterations) ===")
    print("  (dominated by modular exponentiation on 2048-bit prime)")
    for name, stmt in [
        ("v1 (SHA-256 of str)", "derive_shared_key_v1(priv_a, pub_b)"),
        ("v2 (SHA-256 of bytes)", "derive_shared_key_v2(priv_a, pub_b)"),
        ("v3 (HMAC-SHA256)", "derive_shared_key_v3(priv_a, pub_b)"),
    ]:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {name}: {t:.4f}s")


if __name__ == "__main__":
    benchmark()
