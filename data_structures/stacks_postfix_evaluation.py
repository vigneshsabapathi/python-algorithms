"""
Reverse Polish Notation (Postfix) evaluation.
https://en.wikipedia.org/wiki/Reverse_Polish_notation
Valid operators: +, -, *, /, ^
"""

UNARY_OP_SYMBOLS = ("-", "+")

OPERATORS = {
    "^": lambda p, q: p**q,
    "*": lambda p, q: p * q,
    "/": lambda p, q: p / q,
    "+": lambda p, q: p + q,
    "-": lambda p, q: p - q,
}


def parse_token(token: str | float) -> float | str:
    """
    Converts token to float if it is a number, else returns as-is.

    >>> parse_token("5")
    5.0
    >>> parse_token("+")
    '+'
    """
    if token in OPERATORS:
        return token
    try:
        return float(token)
    except ValueError:
        msg = f"{token} is neither a number nor a valid operator"
        raise ValueError(msg)


def evaluate(post_fix: list[str], verbose: bool = False) -> float:
    """
    Evaluate postfix expression using a stack.

    >>> evaluate(["0"])
    0.0
    >>> evaluate(["-0"])
    -0.0
    >>> evaluate(["1"])
    1.0
    >>> evaluate(["-1"])
    -1.0
    >>> evaluate(["-1.1"])
    -1.1
    >>> evaluate(["2", "1", "+", "3", "*"])
    9.0
    >>> evaluate(["2", "1.9", "+", "3", "*"])
    11.7
    >>> evaluate(["4", "13", "5", "/", "+"])
    6.6
    >>> evaluate(["2", "-", "3", "+"])
    1.0
    >>> evaluate(["-4", "5", "*", "6", "-"])
    -26.0
    >>> evaluate([])
    0
    >>> evaluate(["4", "-", "6", "7", "/", "9", "8"])
    Traceback (most recent call last):
    ...
    ArithmeticError: Input is not a valid postfix expression
    """
    if not post_fix:
        return 0
    valid_expression = [parse_token(token) for token in post_fix]
    if verbose:
        print("Symbol".center(8), "Action".center(12), "Stack", sep=" | ")
        print("-" * (30 + len(post_fix)))
    stack = []
    for x in valid_expression:
        if x not in OPERATORS:
            stack.append(x)
            if verbose:
                print(f"{x}".rjust(8), f"push({x})".ljust(12), stack, sep=" | ")
            continue
        if x in UNARY_OP_SYMBOLS and len(stack) < 2:
            b = stack.pop()
            if x == "-":
                b *= -1
            stack.append(b)
            if verbose:
                print("".rjust(8), f"pop({b})".ljust(12), stack, sep=" | ")
                print(str(x).rjust(8), f"push({x}{b})".ljust(12), stack, sep=" | ")
            continue
        b = stack.pop()
        if verbose:
            print("".rjust(8), f"pop({b})".ljust(12), stack, sep=" | ")
        a = stack.pop()
        if verbose:
            print("".rjust(8), f"pop({a})".ljust(12), stack, sep=" | ")
        stack.append(OPERATORS[x](a, b))
        if verbose:
            print(f"{x}".rjust(8), f"push({a}{x}{b})".ljust(12), stack, sep=" | ")
    if len(stack) != 1:
        raise ArithmeticError("Input is not a valid postfix expression")
    return float(stack[0])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    expression = "5 6 9 * +".split()
    print(f"Result: {evaluate(expression, verbose=True)}")
