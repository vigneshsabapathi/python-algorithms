"""Max sum sliding window — variants + benchmark."""

import time
import random


def brute_force(nums, k):
    best = float("-inf")
    for i in range(len(nums) - k + 1):
        s = sum(nums[i : i + k])
        if s > best:
            best = s
    return best


def sliding_window(nums, k):
    w = sum(nums[:k])
    best = w
    for i in range(k, len(nums)):
        w += nums[i] - nums[i - k]
        if w > best:
            best = w
    return best


def prefix_sum(nums, k):
    n = len(nums)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + nums[i]
    best = float("-inf")
    for i in range(n - k + 1):
        s = pref[i + k] - pref[i]
        if s > best:
            best = s
    return best


def benchmark():
    n, k = 100_000, 500
    data = [random.randint(-1000, 1000) for _ in range(n)]
    for name, fn in [
        ("brute_force", brute_force),
        ("sliding_window", sliding_window),
        ("prefix_sum", prefix_sum),
    ]:
        start = time.perf_counter()
        r = fn(data, k)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:18s} result={r}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
