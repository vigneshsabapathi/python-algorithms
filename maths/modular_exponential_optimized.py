"""Modular exponentiation — variants + benchmark."""

import time
import random


def mod_exp_naive(base, exp, mod):
    r = 1
    for _ in range(exp):
        r = (r * base) % mod
    return r


def mod_exp_binary_iter(base, exp, mod):
    if mod == 1:
        return 0
    r = 1
    base %= mod
    while exp:
        if exp & 1:
            r = (r * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return r


def mod_exp_recursive(base, exp, mod):
    if exp == 0:
        return 1
    half = mod_exp_recursive(base, exp // 2, mod)
    half = (half * half) % mod
    if exp & 1:
        half = (half * base) % mod
    return half


def mod_exp_builtin(base, exp, mod):
    return pow(base, exp, mod)


def benchmark():
    base, exp, mod = 7, 10**6, 10**9 + 7
    for name, fn in [
        ("binary_iterative", mod_exp_binary_iter),
        ("binary_recursive", mod_exp_recursive),
        ("pow_builtin", mod_exp_builtin),
    ]:
        start = time.perf_counter()
        for _ in range(1000):
            fn(base, exp, mod)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} time={elapsed:.3f} ms")
    # Naive only for small exp
    start = time.perf_counter()
    for _ in range(100):
        mod_exp_naive(base, 10_000, mod)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'naive_loop(exp=10k)':20s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
