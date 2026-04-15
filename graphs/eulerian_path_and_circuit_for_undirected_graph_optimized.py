"""
Eulerian Path / Circuit - Optimized Variants with Benchmarks.

Variant 1: Degree-parity check (is Eulerian?)
Variant 2: Hierholzer's algorithm (construct the actual tour)
Variant 3: Fleury's algorithm (construct, O(E^2))

>>> eulerian_type({0: [1, 2], 1: [0, 2], 2: [0, 1]})
'circuit'
>>> tour = hierholzer({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
>>> len(tour) == 4
True
>>> tour2 = fleury({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0)
>>> len(tour2) == 4
True
"""

import time
import random
from collections import defaultdict


def eulerian_type(graph):
    """Return 'circuit', 'path', or 'none'.

    >>> eulerian_type({0: [1], 1: [0]})
    'path'
    """
    if not graph:
        return "none"
    non_iso = [v for v in graph if graph[v]]
    if not non_iso:
        return "none"
    start = non_iso[0]
    visited = {start}
    st = [start]
    while st:
        u = st.pop()
        for v in graph[u]:
            if v not in visited:
                visited.add(v)
                st.append(v)
    if any(v not in visited for v in non_iso):
        return "none"
    odd = sum(1 for v in graph if len(graph[v]) % 2)
    if odd == 0:
        return "circuit"
    if odd == 2:
        return "path"
    return "none"


def hierholzer(graph, start):
    """Construct an Eulerian tour using Hierholzer's algorithm.

    >>> hierholzer({0: [1], 1: [0]}, 0)
    [0, 1]
    """
    # Work on a copy with multiedge support
    adj = {u: list(vs) for u, vs in graph.items()}
    stack = [start]
    circuit = []
    while stack:
        u = stack[-1]
        if adj.get(u):
            v = adj[u].pop()
            adj[v].remove(u)
            stack.append(v)
        else:
            circuit.append(stack.pop())
    return circuit[::-1]


def _bridge_count(adj, start):
    """Count vertices reachable from start (for bridge test)."""
    seen = {start}
    st = [start]
    while st:
        u = st.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                st.append(v)
    return len(seen)


def fleury(graph, start):
    """Fleury's algorithm. O(E^2) due to bridge checks.

    >>> fleury({0: [1], 1: [0]}, 0)
    [0, 1]
    """
    adj = {u: list(vs) for u, vs in graph.items()}
    path = [start]
    u = start
    while adj[u]:
        chosen = None
        for v in adj[u]:
            # Prefer non-bridge
            adj[u].remove(v)
            adj[v].remove(u)
            before = _bridge_count(adj, u) if adj[u] else 0
            after = _bridge_count(adj, v)
            adj[u].append(v)
            adj[v].append(u)
            if not adj[u] or before <= after:
                chosen = v
                break
        if chosen is None:
            chosen = adj[u][0]
        adj[u].remove(chosen)
        adj[chosen].remove(u)
        path.append(chosen)
        u = chosen
    return path


def _random_eulerian(n, extra_cycles=3):
    """Build a connected graph where every vertex has even degree."""
    random.seed(0)
    adj = defaultdict(list)
    verts = list(range(n))
    random.shuffle(verts)
    # Base cycle
    for i in range(n):
        u, v = verts[i], verts[(i + 1) % n]
        adj[u].append(v)
        adj[v].append(u)
    # Extra cycles
    for _ in range(extra_cycles):
        cyc = random.sample(verts, 4)
        for i in range(4):
            u, v = cyc[i], cyc[(i + 1) % 4]
            adj[u].append(v)
            adj[v].append(u)
    return dict(adj)


def benchmark():
    g = _random_eulerian(200)
    variants = [
        ("Degree check", lambda: eulerian_type(g)),
        ("Hierholzer tour", lambda: hierholzer(g, next(iter(g)))),
        ("Fleury tour", lambda: fleury(g, next(iter(g)))),
    ]
    print(f"Benchmark: Eulerian on n=200 vertices")
    print("-" * 65)
    for name, fn in variants:
        t0 = time.perf_counter()
        for _ in range(3):
            r = fn()
        dt = (time.perf_counter() - t0) * 1000 / 3
        sz = len(r) if isinstance(r, list) else r
        print(f"{name:<18} result_size={sz}   time={dt:.3f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
