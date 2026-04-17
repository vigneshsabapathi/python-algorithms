"""
Shuffled Shift Cipher — Optimized Variants & Benchmark
========================================================
Compares the full ShuffledShiftCipher class vs lightweight functional variants.
"""

import timeit
from ciphers.shuffled_shift_cipher import ShuffledShiftCipher


# Variant 1: Original class-based (reference)
def encrypt_v1_factory(passcode: str):
    cipher = ShuffledShiftCipher(passcode)
    return cipher.encrypt, cipher.decrypt


# Variant 2: Prebuilt key_list + shift key stored externally
def _make_key(passcode: str):
    import string
    key_list_opts = string.ascii_letters + string.digits + string.punctuation + " \t\n"
    keys_l: list[str] = []
    breakpoints = sorted(set(passcode))
    temp: list[str] = []
    for c in key_list_opts:
        temp.append(c)
        if c in breakpoints or c == key_list_opts[-1]:
            keys_l.extend(temp[::-1])
            temp.clear()
    nums = [ord(x) for x in passcode]
    for i in range(1, len(nums), 2):
        nums[i] *= -1
    shift = sum(nums)
    if shift <= 0:
        shift = len(passcode)
    return keys_l, shift


def encrypt_v2(plaintext: str, key_list: list[str], shift: int) -> str:
    n = len(key_list)
    return "".join(key_list[(key_list.index(c) + shift) % n] for c in plaintext)


def decrypt_v2(ciphertext: str, key_list: list[str], shift: int) -> str:
    n = len(key_list)
    return "".join(key_list[(key_list.index(c) - shift) % -n] for c in ciphertext)


def benchmark(n: int = 1_000) -> None:
    pc = "4PYIXyqeQZr44"
    msg = "Hello, this is a test"
    enc_v1, dec_v1 = encrypt_v1_factory(pc)
    key_list, shift = _make_key(pc)

    t1 = timeit.timeit(lambda: enc_v1(msg), number=n)
    t2 = timeit.timeit(lambda: encrypt_v2(msg, key_list, shift), number=n)
    print(f"V1 (class method) : {t1:.4f}s for {n:,} runs")
    print(f"V2 (prebuilt key) : {t2:.4f}s for {n:,} runs")


if __name__ == "__main__":
    pc = "4PYIXyqeQZr44"
    msg = "Hello"
    enc, dec = encrypt_v1_factory(pc)
    encoded = enc(msg)
    print("V1 encrypted:", encoded)
    print("V1 decrypted:", dec(encoded))

    key_list, shift = _make_key(pc)
    enc2 = encrypt_v2(msg, key_list, shift)
    print("V2 encrypted:", enc2)
    print("V2 decrypted:", decrypt_v2(enc2, key_list, shift))
    benchmark()
