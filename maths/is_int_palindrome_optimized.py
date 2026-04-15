"""Integer palindrome — variants + benchmark."""

import time
import random


def pal_string(n):
    if n < 0:
        return False
    s = str(n)
    return s == s[::-1]


def pal_half_reverse(n):
    if n < 0 or (n % 10 == 0 and n != 0):
        return False
    r = 0
    while n > r:
        r = r * 10 + n % 10
        n //= 10
    return n == r or n == r // 10


def pal_full_reverse(n):
    if n < 0:
        return False
    original, rev = n, 0
    while n > 0:
        rev = rev * 10 + n % 10
        n //= 10
    return original == rev


def benchmark():
    data = [random.randint(0, 10**12) for _ in range(100_000)]
    # Sprinkle some palindromes
    for i in range(0, len(data), 100):
        data[i] = 1234321
    for name, fn in [
        ("string_reverse", pal_string),
        ("half_reverse_math", pal_half_reverse),
        ("full_reverse_math", pal_full_reverse),
    ]:
        start = time.perf_counter()
        hits = sum(1 for v in data if fn(v))
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} palindromes={hits}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
