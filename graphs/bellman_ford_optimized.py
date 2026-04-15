"""
Bellman-Ford - Optimized Variants with Benchmarks.

Variant 1: Standard Bellman-Ford with early termination
Variant 2: SPFA (Shortest Path Faster Algorithm) - queue-based optimization
Variant 3: Yen's optimization (alternating forward/backward relaxation)

>>> edges = [(0,1,4), (0,2,5), (1,2,-3), (2,3,3), (3,1,1)]
>>> bf_standard(4, edges, 0)
{0: 0, 1: 4, 2: 1, 3: 4}
>>> bf_spfa(4, edges, 0)
{0: 0, 1: 4, 2: 1, 3: 4}
>>> bf_yen(4, edges, 0)
{0: 0, 1: 4, 2: 1, 3: 4}
"""

import time
from collections import deque
from math import inf


# --- Variant 1: Standard with early termination ---
def bf_standard(
    n: int, edges: list[tuple[int, int, float]], source: int
) -> dict[int, float]:
    """
    Standard Bellman-Ford with early termination.

    >>> bf_standard(3, [(0,1,1),(1,2,2)], 0)
    {0: 0, 1: 1, 2: 3}
    """
    dist = {i: inf for i in range(n)}
    dist[source] = 0
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            raise ValueError("Negative cycle detected")
    return dist


# --- Variant 2: SPFA (queue-based Bellman-Ford) ---
def bf_spfa(
    n: int, edges: list[tuple[int, int, float]], source: int
) -> dict[int, float]:
    """
    SPFA: Only relaxes edges from recently-updated vertices.
    Average O(E), worst O(VE) like standard.

    >>> bf_spfa(3, [(0,1,1),(1,2,2)], 0)
    {0: 0, 1: 1, 2: 3}
    """
    from collections import defaultdict

    adj: dict[int, list[tuple[int, float]]] = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = {i: inf for i in range(n)}
    dist[source] = 0
    in_queue = [False] * n
    count = [0] * n  # relaxation count for negative cycle detection
    queue = deque([source])
    in_queue[source] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False

        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                count[v] += 1
                if count[v] >= n:
                    raise ValueError("Negative cycle detected")
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True

    return dist


# --- Variant 3: Yen's optimization ---
def bf_yen(
    n: int, edges: list[tuple[int, int, float]], source: int
) -> dict[int, float]:
    """
    Yen's improvement: partition edges and alternate relaxation direction.
    Empirically converges faster than standard on many graphs.

    >>> bf_yen(3, [(0,1,1),(1,2,2)], 0)
    {0: 0, 1: 1, 2: 3}
    """
    dist = {i: inf for i in range(n)}
    dist[source] = 0

    # Partition edges: forward (u < v) and backward (u > v)
    forward = [(u, v, w) for u, v, w in edges if u <= v]
    backward = [(u, v, w) for u, v, w in edges if u > v]

    for _ in range(n - 1):
        updated = False
        # Forward pass
        for u, v, w in forward:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        # Backward pass
        for u, v, w in backward:
            if dist[u] != inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    for u, v, w in edges:
        if dist[u] != inf and dist[u] + w < dist[v]:
            raise ValueError("Negative cycle detected")
    return dist


def benchmark() -> None:
    """Benchmark all variants."""
    import random
    random.seed(42)
    n = 500
    edges = []
    # Connected graph
    for i in range(1, n):
        j = random.randint(0, i - 1)
        w = random.randint(-5, 20)
        edges.append((j, i, w))
    # Extra edges
    for _ in range(n * 3):
        u, v = random.randint(0, n - 1), random.randint(0, n - 1)
        if u != v:
            edges.append((u, v, random.randint(1, 20)))

    variants = [
        ("Standard BF", lambda: bf_standard(n, edges, 0)),
        ("SPFA", lambda: bf_spfa(n, edges, 0)),
        ("Yen's BF", lambda: bf_yen(n, edges, 0)),
    ]

    print(f"\nBenchmark: Bellman-Ford on {n}-node, {len(edges)}-edge graph")
    print("-" * 55)
    for name, func in variants:
        t0 = time.perf_counter()
        for _ in range(5):
            result = func()
        elapsed = (time.perf_counter() - t0) / 5
        reachable = sum(1 for d in result.values() if d != inf)
        print(f"{name:<20} reachable={reachable:<5} time={elapsed*1000:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
