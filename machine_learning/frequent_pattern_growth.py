"""
Frequent Pattern Growth (FP-Growth)

Efficient frequent itemset mining without candidate generation.
Builds a compressed FP-tree and mines patterns via conditional
pattern bases.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/frequent_pattern_growth.py
"""

from collections import defaultdict


class FPNode:
    """Node in an FP-tree."""

    def __init__(self, item: str | None = None, count: int = 0, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children: dict[str, FPNode] = {}
        self.next: FPNode | None = None  # link to next node with same item


class FPTree:
    """
    FP-Tree for frequent pattern mining.

    >>> transactions = [
    ...     ['a', 'b', 'c'],
    ...     ['a', 'b'],
    ...     ['a', 'c'],
    ...     ['b', 'c'],
    ...     ['a', 'b', 'c'],
    ... ]
    >>> tree = FPTree(transactions, min_support=2)
    >>> patterns = tree.mine_patterns()
    >>> frozenset(['a', 'b']) in [frozenset(p) for p in patterns]
    True
    """

    def __init__(
        self, transactions: list[list[str]], min_support: int = 2
    ) -> None:
        self.min_support = min_support
        self.root = FPNode()
        self.header_table: dict[str, FPNode | None] = {}
        self.item_counts: dict[str, int] = defaultdict(int)

        # Count item frequencies
        for transaction in transactions:
            for item in transaction:
                self.item_counts[item] += 1

        # Filter infrequent items
        self.item_counts = {
            k: v for k, v in self.item_counts.items() if v >= min_support
        }

        # Build tree
        for transaction in transactions:
            # Sort by frequency (descending), filter infrequent
            filtered = [
                item for item in transaction if item in self.item_counts
            ]
            filtered.sort(key=lambda x: (-self.item_counts[x], x))
            self._insert_tree(filtered, self.root)

    def _insert_tree(self, items: list[str], node: FPNode) -> None:
        """Insert a transaction into the FP-tree."""
        if not items:
            return
        item = items[0]
        if item in node.children:
            node.children[item].count += 1
        else:
            new_node = FPNode(item=item, count=1, parent=node)
            node.children[item] = new_node
            # Update header table
            if item not in self.header_table:
                self.header_table[item] = new_node
            else:
                current = self.header_table[item]
                while current.next is not None:
                    current = current.next
                current.next = new_node
        self._insert_tree(items[1:], node.children[item])

    def _get_prefix_paths(self, item: str) -> list[tuple[list[str], int]]:
        """Get all prefix paths ending at nodes for given item."""
        paths = []
        node = self.header_table.get(item)
        while node is not None:
            path = []
            parent = node.parent
            while parent is not None and parent.item is not None:
                path.append(parent.item)
                parent = parent.parent
            if path:
                paths.append((path[::-1], node.count))
            node = node.next
        return paths

    def mine_patterns(self) -> dict[tuple[str, ...], int]:
        """
        Mine all frequent patterns from the FP-tree.

        Returns dict mapping patterns (tuples) to their support counts.
        """
        patterns: dict[tuple[str, ...], int] = {}
        self._mine_tree(self.root, [], patterns)
        return patterns

    def _mine_tree(
        self,
        tree_root: FPNode,
        prefix: list[str],
        patterns: dict[tuple[str, ...], int],
    ) -> None:
        """Recursively mine patterns."""
        # Sort items by frequency (ascending) for bottom-up mining
        sorted_items = sorted(
            self.item_counts.keys(),
            key=lambda x: self.item_counts[x],
        )

        for item in sorted_items:
            if item not in self.header_table:
                continue

            new_pattern = prefix + [item]
            support = 0
            node = self.header_table[item]
            while node is not None:
                support += node.count
                node = node.next

            if support >= self.min_support:
                patterns[tuple(sorted(new_pattern))] = support

                # Build conditional FP-tree
                prefix_paths = self._get_prefix_paths(item)
                if prefix_paths:
                    cond_transactions = []
                    for path, count in prefix_paths:
                        for _ in range(count):
                            cond_transactions.append(path)

                    if cond_transactions:
                        cond_tree = FPTree(cond_transactions, self.min_support)
                        cond_tree._mine_tree(
                            cond_tree.root, new_pattern, patterns
                        )


def fp_growth(
    transactions: list[list[str]], min_support: int = 2
) -> dict[tuple[str, ...], int]:
    """
    FP-Growth algorithm for frequent itemset mining.

    >>> transactions = [
    ...     ['bread', 'milk'],
    ...     ['bread', 'eggs'],
    ...     ['milk', 'eggs'],
    ...     ['bread', 'milk', 'eggs'],
    ...     ['bread', 'milk'],
    ... ]
    >>> patterns = fp_growth(transactions, min_support=2)
    >>> ('bread', 'milk') in patterns
    True
    >>> patterns[('bread', 'milk')] >= 2
    True
    """
    tree = FPTree(transactions, min_support)
    return tree.mine_patterns()


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- FP-Growth Demo ---")
    transactions = [
        ["bread", "milk", "eggs"],
        ["bread", "butter"],
        ["milk", "butter"],
        ["bread", "milk", "butter"],
        ["bread", "milk"],
        ["milk", "eggs"],
        ["bread", "eggs"],
        ["bread", "milk", "eggs", "butter"],
    ]

    print(f"Transactions: {len(transactions)}")
    patterns = fp_growth(transactions, min_support=2)

    print(f"\nFrequent patterns (min_support=2):")
    for pattern, support in sorted(patterns.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {set(pattern)}: support={support}")
