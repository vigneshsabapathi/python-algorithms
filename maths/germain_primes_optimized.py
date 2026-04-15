"""Germain primes — variants + benchmark."""

import time


def _sieve(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return sieve


def germain_trial(limit):
    def is_prime(n):
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0:
            return False
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True

    return [p for p in range(2, limit + 1) if is_prime(p) and is_prime(2 * p + 1)]


def germain_sieve(limit):
    s = _sieve(2 * limit + 2)
    return [p for p in range(2, limit + 1) if s[p] and s[2 * p + 1]]


def germain_sieve_numpy(limit):
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return germain_sieve(limit)
    sieve = np.ones(2 * limit + 3, dtype=bool)
    sieve[:2] = False
    for i in range(2, int((2 * limit + 2) ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False
    result = []
    for p in range(2, limit + 1):
        if sieve[p] and sieve[2 * p + 1]:
            result.append(p)
    return result


def benchmark():
    limit = 20_000
    for name, fn in [
        ("trial_division", germain_trial),
        ("sieve_bool", germain_sieve),
        ("sieve_numpy", germain_sieve_numpy),
    ]:
        start = time.perf_counter()
        r = fn(limit)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} count={len(r)}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
