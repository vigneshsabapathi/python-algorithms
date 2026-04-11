"""
Boyer-Moore Majority Vote Algorithm — Find the majority element in O(n) time, O(1) space.

A majority element appears more than n/2 times. The algorithm works in two passes:
1. Find a candidate using a counter.
2. Verify the candidate actually has majority.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/majority_vote_algorithm.py
"""

from __future__ import annotations


def majority_vote(votes: list[int]) -> int | None:
    """
    Find the majority element (appears > n/2 times) using Boyer-Moore voting.

    Returns None if no majority element exists.

    >>> majority_vote([1, 1, 1, 2, 2])
    1
    >>> majority_vote([2, 2, 1, 1, 1, 2, 2])
    2
    >>> majority_vote([1, 2, 3])
    >>> majority_vote([1])
    1
    >>> majority_vote([])
    >>> majority_vote([3, 3, 3, 3])
    3
    """
    if not votes:
        return None

    # Phase 1: Find candidate
    candidate = votes[0]
    count = 0

    for vote in votes:
        if count == 0:
            candidate = vote
        count += 1 if vote == candidate else -1

    # Phase 2: Verify candidate has majority
    if votes.count(candidate) > len(votes) // 2:
        return candidate

    return None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
