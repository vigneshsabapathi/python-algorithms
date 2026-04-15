"""
FP-GraphMiner - Optimized Variants

Frequent Pattern Graph Mining compactly represents network graphs as a Frequent
Pattern Graph (FP-Graph) for mining frequent subgraphs.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/frequent_pattern_graph_miner.py
"""

import time
from collections import defaultdict


# ---------- Sample data ----------
edge_array = [
    ['ab-e1', 'ac-e3', 'ad-e5', 'bc-e4', 'bd-e2', 'be-e6', 'bh-e12', 'cd-e2',
     'ce-e4', 'de-e1', 'df-e8', 'dg-e5', 'dh-e10', 'ef-e3', 'eg-e2', 'fg-e6',
     'gh-e6', 'hi-e3'],
    ['ab-e1', 'ac-e3', 'ad-e5', 'bc-e4', 'bd-e2', 'be-e6', 'cd-e2', 'de-e1',
     'df-e8', 'ef-e3', 'eg-e2', 'fg-e6'],
    ['ab-e1', 'ac-e3', 'bc-e4', 'bd-e2', 'de-e1', 'df-e8', 'dg-e5', 'ef-e3',
     'eg-e2', 'eh-e12', 'fg-e6', 'fh-e10', 'gh-e6'],
    ['ab-e1', 'ac-e3', 'bc-e4', 'bd-e2', 'bh-e12', 'cd-e2', 'df-e8', 'dh-e10'],
    ['ab-e1', 'ac-e3', 'ad-e5', 'bc-e4', 'bd-e2', 'cd-e2', 'ce-e4', 'de-e1',
     'df-e8', 'dg-e5', 'ef-e3', 'eg-e2', 'fg-e6'],
]


# ---------- Variant 1: Set-based distinct edge extraction ----------
def get_distinct_edges_set(edge_array: list[list[str]]) -> set[str]:
    """
    Extract distinct node-pair labels using set comprehension.

    >>> sorted(get_distinct_edges_set([['ab-e1', 'bc-e2'], ['cd-e3']]))
    ['ab', 'bc', 'cd']
    """
    return {item.split('-')[0] for row in edge_array for item in row}


# ---------- Variant 2: Dict-based frequency with bitwise operations ----------
def get_frequency_table_optimized(edge_array: list[list[str]]) -> list[tuple[str, int, str]]:
    """
    Build frequency table with optimized lookups.

    >>> table = get_frequency_table_optimized([['ab-e1', 'bc-e2'], ['ab-e1', 'cd-e3']])
    >>> table[0][1]  # highest frequency first
    2
    """
    n = len(edge_array)
    # Build sets per graph for O(1) lookup
    graph_edges = [set() for _ in range(n)]
    all_edges = set()
    for i, row in enumerate(edge_array):
        for item in row:
            label = item.split('-')[0]
            graph_edges[i].add(label)
            all_edges.add(label)

    freq_table = []
    for edge in all_edges:
        bitcode = ''.join('1' if edge in graph_edges[i] else '0' for i in range(n))
        count = bitcode.count('1')
        freq_table.append((edge, count, bitcode))

    freq_table.sort(key=lambda x: x[1], reverse=True)
    return freq_table


# ---------- Variant 3: Counter-based support calculation ----------
def get_support_from_table(freq_table: list[tuple[str, int, str]], n_graphs: int) -> dict[str, float]:
    """
    Calculate support percentage for each edge pattern.

    >>> table = [('ab', 3, '111'), ('cd', 2, '110')]
    >>> get_support_from_table(table, 3)
    {'ab': 100.0, 'cd': 66.67}
    """
    return {
        edge: round(count / n_graphs * 100, 2)
        for edge, count, _ in freq_table
    }


def preprocess(edge_array: list[list[str]]) -> list[list[list[str]]]:
    """Split edge labels into [node_pair, edge_label] format."""
    return [[item.split('-') for item in row] for row in edge_array]


# ---------- Benchmark ----------
def benchmark():
    results = {}

    # Original approach
    start = time.perf_counter()
    for _ in range(1000):
        distinct = set()
        for row in edge_array:
            for item in row:
                t = item.split('-')
                distinct.add(t[0])
    elapsed = (time.perf_counter() - start) / 1000 * 1000
    results['original_distinct'] = elapsed
    print(f"  {'original_distinct':25s}: {elapsed:.4f} ms")

    # Set-based
    start = time.perf_counter()
    for _ in range(1000):
        get_distinct_edges_set(edge_array)
    elapsed = (time.perf_counter() - start) / 1000 * 1000
    results['set_based_distinct'] = elapsed
    print(f"  {'set_based_distinct':25s}: {elapsed:.4f} ms")

    # Frequency table
    start = time.perf_counter()
    for _ in range(1000):
        get_frequency_table_optimized(edge_array)
    elapsed = (time.perf_counter() - start) / 1000 * 1000
    results['optimized_freq_table'] = elapsed
    print(f"  {'optimized_freq_table':25s}: {elapsed:.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== FP-GraphMiner Benchmark (1000 runs) ===")
    benchmark()
