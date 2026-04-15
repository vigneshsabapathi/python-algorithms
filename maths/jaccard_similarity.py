"""
Jaccard similarity: |A ∩ B| / |A ∪ B|. Range [0, 1].
Applications: document similarity, clustering, set comparison.

>>> jaccard_similarity({1, 2, 3}, {2, 3, 4})
0.5
>>> jaccard_similarity({"a", "b"}, {"a", "b"})
1.0
>>> jaccard_similarity(set(), set())
1.0
>>> jaccard_similarity({1}, {2})
0.0
"""


def jaccard_similarity(a: set, b: set) -> float:
    """Standard Jaccard on sets. Convention: J(∅, ∅) = 1.

    >>> jaccard_similarity({1, 2, 3, 4}, {3, 4, 5, 6})
    0.3333333333333333
    """
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union


def jaccard_similarity_strings(s1: str, s2: str) -> float:
    """Jaccard over characters of two strings."""
    return jaccard_similarity(set(s1), set(s2))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(jaccard_similarity({1, 2, 3}, {2, 3, 4}))
