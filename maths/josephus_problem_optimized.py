"""Josephus — variants + benchmark."""

import time
from collections import deque


def jos_iter(n, k):
    s = 0
    for i in range(2, n + 1):
        s = (s + k) % i
    return s


def jos_simulation_list(n, k):
    people = list(range(n))
    idx = 0
    while len(people) > 1:
        idx = (idx + k - 1) % len(people)
        people.pop(idx)
    return people[0]


def jos_simulation_deque(n, k):
    q = deque(range(n))
    while len(q) > 1:
        q.rotate(-(k - 1))
        q.popleft()
    return q[0]


def benchmark():
    n, k = 20_000, 7
    for name, fn in [
        ("recurrence", jos_iter),
        ("sim_list_pop", jos_simulation_list),
        ("sim_deque_rotate", jos_simulation_deque),
    ]:
        start = time.perf_counter()
        r = fn(n, k)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} survivor={r}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
