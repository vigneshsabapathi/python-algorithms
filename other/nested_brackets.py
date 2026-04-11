"""
Nested Brackets — Check if brackets/parentheses are balanced.

Validates that every opening bracket has a matching closing bracket
in the correct order. Supports (), [], {}.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/nested_brackets.py
"""

from __future__ import annotations


def is_balanced(expression: str) -> bool:
    """
    Check if brackets in the expression are balanced.

    >>> is_balanced("([])")
    True
    >>> is_balanced("([)]")
    False
    >>> is_balanced("{[()]}")
    True
    >>> is_balanced("")
    True
    >>> is_balanced("((()))")
    True
    >>> is_balanced("(")
    False
    >>> is_balanced(")")
    False
    >>> is_balanced("{[}]")
    False
    >>> is_balanced("a(b[c]d)e")
    True
    """
    matching = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []

    for char in expression:
        if char in "([{":
            stack.append(char)
        elif char in ")]}":
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()

    return len(stack) == 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
