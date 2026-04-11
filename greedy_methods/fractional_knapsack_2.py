"""
Fractional Knapsack 2 — Object-oriented approach

Uses a named-tuple / class-based item representation. Same greedy algorithm
but structured differently for interview discussions about design.

Reference: https://github.com/TheAlgorithms/Python/blob/master/greedy_methods/fractional_knapsack_2.py

>>> items = [Item("A", 60, 10), Item("B", 100, 20), Item("C", 120, 30)]
>>> fractional_knapsack(items, 50)
240.0
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Item:
    """Represents an item with a name, value, and weight.

    >>> Item("gold", 500, 10)
    Item(name='gold', value=500, weight=10)
    """

    name: str
    value: int
    weight: int

    @property
    def ratio(self) -> float:
        """Value-to-weight ratio.

        >>> Item("gold", 500, 10).ratio
        50.0
        """
        return self.value / self.weight if self.weight > 0 else float("inf")


def fractional_knapsack(items: list[Item], capacity: int) -> float:
    """
    Greedy fractional knapsack using Item dataclass.

    >>> items = [Item("A", 60, 10), Item("B", 100, 20), Item("C", 120, 30)]
    >>> fractional_knapsack(items, 50)
    240.0
    >>> fractional_knapsack(items, 60)
    280.0
    >>> fractional_knapsack([], 50)
    0.0
    >>> fractional_knapsack(items, 0)
    0.0
    >>> fractional_knapsack([Item("X", 500, 30)], 10)
    166.66666666666666
    """
    sorted_items = sorted(items, key=lambda item: item.ratio, reverse=True)
    total_value = 0.0
    remaining = capacity

    for item in sorted_items:
        if remaining <= 0:
            break
        if item.weight <= remaining:
            total_value += item.value
            remaining -= item.weight
        else:
            total_value += item.value * (remaining / item.weight)
            remaining = 0

    return total_value


if __name__ == "__main__":
    import doctest

    doctest.testmod()
