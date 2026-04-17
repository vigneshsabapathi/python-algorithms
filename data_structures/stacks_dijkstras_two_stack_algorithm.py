"""
Dijkstra's Two Stack Algorithm for evaluating mathematical expressions.
https://medium.com/@haleesammar/implemented-in-js-dijkstras-2-stack-algorithm-for-evaluating-mathematical-expressions-fc0837dae1ea

We can use Dijkstra's two stack algorithm to solve an equation
such as: (5 + ((4 * 2) * (2 + 3)))

RULES:
1. Operand encountered -> push to operand stack.
2. Operator encountered -> push to operator stack.
3. Left parenthesis encountered -> ignore it.
4. Right parenthesis encountered -> pop operator, pop two operands,
   compute result, push result to operand stack.
5. End of expression -> result is on operand stack.

NOTE: Only works with whole numbers.
"""

__author__ = "Alexander Joslin"

import operator as op
from stacks_stack import Stack


def dijkstras_two_stack_algorithm(equation: str) -> int:
    """
    >>> dijkstras_two_stack_algorithm("(5 + 3)")
    8
    >>> dijkstras_two_stack_algorithm("((9 - (2 + 9)) + (8 - 1))")
    5
    >>> dijkstras_two_stack_algorithm("((((3 - 2) - (2 + 3)) + (2 - 4)) + 3)")
    -3
    """
    operators = {"*": op.mul, "/": op.truediv, "+": op.add, "-": op.sub}

    operand_stack: Stack = Stack()
    operator_stack: Stack = Stack()

    for i in equation:
        if i.isdigit():
            operand_stack.push(int(i))
        elif i in operators:
            operator_stack.push(i)
        elif i == ")":
            opr = operator_stack.peek()
            operator_stack.pop()
            num1 = operand_stack.peek()
            operand_stack.pop()
            num2 = operand_stack.peek()
            operand_stack.pop()

            total = operators[opr](num2, num1)
            operand_stack.push(total)

    return operand_stack.peek()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    equation = "(5 + ((4 * 2) * (2 + 3)))"
    print(f"{equation} = {dijkstras_two_stack_algorithm(equation)}")
