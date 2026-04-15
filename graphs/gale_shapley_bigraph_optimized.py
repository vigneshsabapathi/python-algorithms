"""
Gale-Shapley Stable Matching - Optimized Variants

Finds stable matching in bipartite graphs where no two elements prefer each other
over their current partners. Classic application: organ donor matching.

Source: https://github.com/TheAlgorithms/Python/blob/master/graphs/gale_shapley_bigraph.py
"""

import time
from collections import deque


# ---------- Variant 1: Deque-based with rank matrix (O(1) preference lookup) ----------
def stable_matching_rank_matrix(
    donor_pref: list[list[int]], recipient_pref: list[list[int]]
) -> list[int]:
    """
    Uses precomputed rank matrix for O(1) preference comparisons.

    >>> donor_pref = [[0, 1, 3, 2], [0, 2, 3, 1], [1, 0, 2, 3], [0, 3, 1, 2]]
    >>> recipient_pref = [[3, 1, 2, 0], [3, 1, 0, 2], [0, 3, 1, 2], [1, 0, 3, 2]]
    >>> stable_matching_rank_matrix(donor_pref, recipient_pref)
    [1, 2, 3, 0]
    """
    n = len(donor_pref)
    # Precompute rank: rank[r][d] = position of donor d in recipient r's preference
    rank = [[0] * n for _ in range(n)]
    for r in range(n):
        for i, d in enumerate(recipient_pref[r]):
            rank[r][d] = i

    free_donors = deque(range(n))
    donor_next = [0] * n
    rec_match = [-1] * n
    donor_match = [-1] * n

    while free_donors:
        d = free_donors.popleft()
        r = donor_pref[d][donor_next[d]]
        donor_next[d] += 1

        if rec_match[r] == -1:
            rec_match[r] = d
            donor_match[d] = r
        elif rank[r][d] < rank[r][rec_match[r]]:
            old_donor = rec_match[r]
            rec_match[r] = d
            donor_match[d] = r
            donor_match[old_donor] = -1
            free_donors.append(old_donor)
        else:
            free_donors.append(d)

    return donor_match


# ---------- Variant 2: Dictionary-based for string labels ----------
def stable_matching_dict(
    proposer_prefs: dict[str, list[str]], responder_prefs: dict[str, list[str]]
) -> dict[str, str]:
    """
    Gale-Shapley with string keys (more readable for real problems).

    >>> props = {'A': ['X', 'Y'], 'B': ['Y', 'X']}
    >>> resps = {'X': ['A', 'B'], 'Y': ['B', 'A']}
    >>> stable_matching_dict(props, resps)
    {'A': 'X', 'B': 'Y'}
    """
    rank = {}
    for r, prefs in responder_prefs.items():
        rank[r] = {p: i for i, p in enumerate(prefs)}

    free = deque(proposer_prefs.keys())
    next_proposal = {p: 0 for p in proposer_prefs}
    match_r = {}
    match_p = {}

    while free:
        p = free.popleft()
        r = proposer_prefs[p][next_proposal[p]]
        next_proposal[p] += 1

        if r not in match_r:
            match_r[r] = p
            match_p[p] = r
        elif rank[r][p] < rank[r][match_r[r]]:
            old = match_r[r]
            match_r[r] = p
            match_p[p] = r
            del match_p[old]
            free.append(old)
        else:
            free.append(p)

    return match_p


# ---------- Variant 3: Original list-based (cleaned up) ----------
def stable_matching_original(
    donor_pref: list[list[int]], recipient_pref: list[list[int]]
) -> list[int]:
    """
    Original algorithm with list-based index lookups.

    >>> donor_pref = [[0, 1, 3, 2], [0, 2, 3, 1], [1, 0, 2, 3], [0, 3, 1, 2]]
    >>> recipient_pref = [[3, 1, 2, 0], [3, 1, 0, 2], [0, 3, 1, 2], [1, 0, 3, 2]]
    >>> stable_matching_original(donor_pref, recipient_pref)
    [1, 2, 3, 0]
    """
    n = len(donor_pref)
    unmatched = list(range(n))
    donor_record = [-1] * n
    rec_record = [-1] * n
    num_donations = [0] * n

    while unmatched:
        donor = unmatched[0]
        recipient = donor_pref[donor][num_donations[donor]]
        num_donations[donor] += 1
        prev_donor = rec_record[recipient]

        if prev_donor != -1:
            if recipient_pref[recipient].index(prev_donor) > recipient_pref[recipient].index(donor):
                rec_record[recipient] = donor
                donor_record[donor] = recipient
                unmatched.append(prev_donor)
                unmatched.remove(donor)
        else:
            rec_record[recipient] = donor
            donor_record[donor] = recipient
            unmatched.remove(donor)
    return donor_record


# ---------- Benchmark ----------
def benchmark():
    import random
    random.seed(42)
    n = 200
    donor_pref = [random.sample(range(n), n) for _ in range(n)]
    recipient_pref = [random.sample(range(n), n) for _ in range(n)]

    for name, fn in [
        ("rank_matrix", lambda: stable_matching_rank_matrix(donor_pref, recipient_pref)),
        ("original", lambda: stable_matching_original(donor_pref, recipient_pref)),
    ]:
        start = time.perf_counter()
        for _ in range(20):
            fn()
        elapsed = (time.perf_counter() - start) / 20 * 1000
        print(f"  {name:20s}: {elapsed:.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Gale-Shapley Benchmark (200 pairs, 20 runs) ===")
    benchmark()
