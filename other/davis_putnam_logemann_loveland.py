"""
Davis-Putnam-Logemann-Loveland (DPLL) — SAT solver algorithm.

A complete, backtracking-based search algorithm for deciding the satisfiability
of propositional logic formulas in conjunctive normal form (CNF).

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/davis_putnam_logemann_loveland.py
"""

from __future__ import annotations


Clause = frozenset[int]  # positive int = variable, negative = negation
Formula = list[Clause]
Assignment = dict[int, bool]


def unit_propagate(formula: Formula, assignment: Assignment) -> Formula | None:
    """Apply unit propagation: if a clause has one literal, it must be true."""
    changed = True
    while changed:
        changed = False
        for clause in formula:
            unset = [lit for lit in clause if abs(lit) not in assignment]
            false_count = sum(
                1
                for lit in clause
                if abs(lit) in assignment
                and assignment[abs(lit)] != (lit > 0)
            )
            if false_count == len(clause):
                return None  # Conflict — clause is unsatisfied
            if len(unset) == 1 and false_count == len(clause) - 1:
                # Unit clause — must assign the remaining literal to true
                lit = unset[0]
                assignment[abs(lit)] = lit > 0
                changed = True

    # Remove satisfied clauses, shrink remaining
    new_formula: Formula = []
    for clause in formula:
        satisfied = any(
            abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
            for lit in clause
        )
        if not satisfied:
            new_clause = frozenset(
                lit for lit in clause if abs(lit) not in assignment
            )
            if not new_clause:
                return None  # Empty clause = conflict
            new_formula.append(new_clause)

    return new_formula


def pure_literal_assign(formula: Formula, assignment: Assignment) -> Formula:
    """Assign pure literals (those appearing with only one polarity)."""
    literal_polarity: dict[int, set[bool]] = {}
    for clause in formula:
        for lit in clause:
            var = abs(lit)
            if var not in assignment:
                literal_polarity.setdefault(var, set()).add(lit > 0)

    for var, polarities in literal_polarity.items():
        if len(polarities) == 1:
            assignment[var] = polarities.pop()

    # Remove satisfied clauses
    new_formula: Formula = []
    for clause in formula:
        satisfied = any(
            abs(lit) in assignment and assignment[abs(lit)] == (lit > 0)
            for lit in clause
        )
        if not satisfied:
            new_formula.append(clause)

    return new_formula


def dpll(formula: Formula, assignment: Assignment | None = None) -> Assignment | None:
    """
    DPLL SAT solver.

    Args:
        formula: List of clauses (each clause is a frozenset of int literals).
                 Positive int = variable true, negative = variable false.
        assignment: Current variable assignments.

    Returns:
        Satisfying assignment dict, or None if unsatisfiable.

    >>> dpll([frozenset([1, 2]), frozenset([-1, 2]), frozenset([1, -2])])
    {1: True, 2: True}
    >>> dpll([frozenset([1]), frozenset([-1])])
    >>> dpll([frozenset([1, -2]), frozenset([2, -3]), frozenset([3])])
    {3: True, 2: True, 1: True}
    """
    if assignment is None:
        assignment = {}

    # Unit propagation
    formula_result = unit_propagate(formula, assignment)
    if formula_result is None:
        return None
    formula = formula_result

    # Pure literal elimination
    formula = pure_literal_assign(formula, assignment)

    # If no clauses remain, formula is satisfied
    if not formula:
        return assignment

    # Choose a variable to branch on (pick from first clause)
    var = abs(next(iter(next(iter(formula)))))

    # Try assigning True
    new_assignment = assignment.copy()
    new_assignment[var] = True
    result = dpll(list(formula), new_assignment)
    if result is not None:
        return result

    # Try assigning False
    new_assignment = assignment.copy()
    new_assignment[var] = False
    return dpll(list(formula), new_assignment)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
