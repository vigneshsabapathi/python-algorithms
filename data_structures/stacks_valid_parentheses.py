"""
Valid parentheses checker using a stack.
LeetCode problem: https://leetcode.com/problems/valid-parentheses/
"""


def is_valid(s: str) -> bool:
    """
    Check if a string of brackets/parentheses is valid.

    >>> is_valid("()")
    True
    >>> is_valid("()[]{}")
    True
    >>> is_valid("(]")
    False
    >>> is_valid("([)]")
    False
    >>> is_valid("{[]}")
    True
    >>> is_valid("")
    True
    >>> is_valid("((")
    False
    """
    stack: list[str] = []
    bracket_map = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map:
            if not stack or stack[-1] != bracket_map[char]:
                return False
            stack.pop()

    return not stack


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    test_cases = ["()", "()[]{}", "(]", "([)]", "{[]}", "", "(("]
    for tc in test_cases:
        print(f"is_valid({tc!r}) = {is_valid(tc)}")
