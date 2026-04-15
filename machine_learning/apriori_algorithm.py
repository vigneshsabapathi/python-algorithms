"""
Apriori Algorithm

Association rule mining algorithm for frequent itemset generation.
Finds sets of items that frequently appear together in transactions.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/apriori_algorithm.py
"""

from itertools import combinations


def generate_candidates(
    prev_frequent: list[frozenset], k: int
) -> list[frozenset]:
    """
    Generate candidate itemsets of size k from frequent itemsets of size k-1.

    >>> prev = [frozenset({1, 2}), frozenset({1, 3}), frozenset({2, 3})]
    >>> sorted([sorted(c) for c in generate_candidates(prev, 3)])
    [[1, 2, 3]]
    """
    candidates = set()
    prev_list = list(prev_frequent)
    for i in range(len(prev_list)):
        for j in range(i + 1, len(prev_list)):
            union = prev_list[i] | prev_list[j]
            if len(union) == k:
                candidates.add(union)
    return list(candidates)


def get_support(
    itemset: frozenset, transactions: list[set]
) -> float:
    """
    Calculate support of an itemset = count / total transactions.

    >>> transactions = [{1, 2, 3}, {1, 2}, {1, 3}, {2, 3}]
    >>> get_support(frozenset({1, 2}), transactions)
    0.5
    """
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)


def apriori(
    transactions: list[set], min_support: float = 0.5
) -> dict[frozenset, float]:
    """
    Apriori algorithm for frequent itemset mining.

    Args:
        transactions: list of sets, each set is a transaction of items
        min_support: minimum support threshold (0 to 1)

    Returns:
        dict mapping frequent itemsets to their support values

    >>> transactions = [{1, 2, 3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]
    >>> result = apriori(transactions, min_support=0.4)
    >>> frozenset({1, 2}) in result
    True
    >>> frozenset({1, 2, 3}) in result
    True
    """
    # Get all unique items
    all_items = set()
    for t in transactions:
        all_items.update(t)

    # Find frequent 1-itemsets
    frequent = {}
    for item in all_items:
        itemset = frozenset({item})
        support = get_support(itemset, transactions)
        if support >= min_support:
            frequent[itemset] = support

    # Current frequent itemsets of size k-1
    current_frequent = [fs for fs in frequent if len(fs) == 1]
    k = 2

    while current_frequent:
        candidates = generate_candidates(current_frequent, k)
        new_frequent = []
        for candidate in candidates:
            support = get_support(candidate, transactions)
            if support >= min_support:
                frequent[candidate] = support
                new_frequent.append(candidate)
        current_frequent = new_frequent
        k += 1

    return frequent


def generate_association_rules(
    frequent_itemsets: dict[frozenset, float],
    min_confidence: float = 0.7,
) -> list[tuple[frozenset, frozenset, float, float]]:
    """
    Generate association rules from frequent itemsets.

    Returns list of (antecedent, consequent, confidence, lift).

    >>> transactions = [{1, 2, 3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}]
    >>> freq = apriori(transactions, min_support=0.4)
    >>> rules = generate_association_rules(freq, min_confidence=0.5)
    >>> len(rules) > 0
    True
    """
    rules = []
    for itemset, support in frequent_itemsets.items():
        if len(itemset) < 2:
            continue
        items = list(itemset)
        for i in range(1, len(items)):
            for antecedent_items in combinations(items, i):
                antecedent = frozenset(antecedent_items)
                consequent = itemset - antecedent

                if antecedent in frequent_itemsets:
                    confidence = support / frequent_itemsets[antecedent]
                    if confidence >= min_confidence:
                        # Lift = confidence / support(consequent)
                        if consequent in frequent_itemsets:
                            lift = confidence / frequent_itemsets[consequent]
                        else:
                            lift = 0.0
                        rules.append((antecedent, consequent, confidence, lift))

    return rules


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Apriori Algorithm Demo ---")
    # Market basket data
    transactions = [
        {"bread", "milk", "eggs"},
        {"bread", "butter"},
        {"milk", "butter"},
        {"bread", "milk", "butter"},
        {"bread", "milk"},
        {"milk", "eggs"},
        {"bread", "eggs"},
        {"bread", "milk", "eggs", "butter"},
    ]

    print(f"Transactions: {len(transactions)}")
    frequent = apriori(transactions, min_support=0.3)

    print(f"\nFrequent itemsets (min_support=0.3):")
    for itemset, support in sorted(frequent.items(), key=lambda x: (-len(x[0]), -x[1])):
        print(f"  {set(itemset)}: support={support:.3f}")

    rules = generate_association_rules(frequent, min_confidence=0.5)
    print(f"\nAssociation rules (min_confidence=0.5):")
    for ant, cons, conf, lift in sorted(rules, key=lambda x: -x[2]):
        print(f"  {set(ant)} -> {set(cons)}: conf={conf:.3f}, lift={lift:.3f}")
