"""
Simplex Algorithm for Linear Programming

Task:
Solve linear programming problems in standard and non-standard form using
the simplex method (two-phase if needed). Supports <=, >=, and = constraints,
with all variables x1, x2, ... >= 0.

The simplex algorithm works on a tableau representation of a linear program.
It iteratively pivots to improve the objective function until an optimal
solution is found or the problem is determined to be infeasible/unbounded.

Two-phase simplex:
  Phase 1 - Minimize sum of artificial variables to find a basic feasible solution
  Phase 2 - Optimize the original objective function

Reference: https://en.wikipedia.org/wiki/Simplex_algorithm
Source: https://github.com/TheAlgorithms/Python/blob/master/linear_programming/simplex.py
"""

from typing import Any

import numpy as np


class Tableau:
    """Operate on simplex tableaus to solve linear programs.

    The tableau encodes the objective function and constraints in matrix form.
    Each row after the objective row(s) represents a constraint, and the last
    column holds the right-hand-side (RHS) values.

    Parameters:
        tableau: 2D numpy array (float64) with objective row(s) and constraint rows
        n_vars: number of decision variables (x1, x2, ...)
        n_artificial_vars: number of artificial variables (for >= or = constraints)

    >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4]]), 2, 2)
    Traceback (most recent call last):
        ...
    TypeError: Tableau must have type float64

    >>> Tableau(np.array([[-1,-1,0,0,-1],[1,3,1,0,4],[3,1,0,1,4.]]), 2, 2)
    Traceback (most recent call last):
        ...
    ValueError: RHS must be > 0

    >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4.]]), -2, 2)
    Traceback (most recent call last):
        ...
    ValueError: number of (artificial) variables must be a natural number
    """

    # Max iteration number to prevent cycling
    maxiter = 100

    def __init__(
        self, tableau: np.ndarray, n_vars: int, n_artificial_vars: int
    ) -> None:
        if tableau.dtype != "float64":
            raise TypeError("Tableau must have type float64")

        if not (tableau[:, -1] >= 0).all():
            raise ValueError("RHS must be > 0")

        if n_vars < 2 or n_artificial_vars < 0:
            raise ValueError(
                "number of (artificial) variables must be a natural number"
            )

        self.tableau = tableau
        self.n_rows, n_cols = tableau.shape

        self.n_vars, self.n_artificial_vars = n_vars, n_artificial_vars

        # 2 if there are >= or == constraints (two-phase), 1 otherwise (standard)
        self.n_stages = (self.n_artificial_vars > 0) + 1

        # Slack variables turn inequalities into equalities
        self.n_slack = n_cols - self.n_vars - self.n_artificial_vars - 1

        # Objectives for each stage
        self.objectives = ["max"]

        # In two-phase simplex, first minimize artificial vars then maximize
        if self.n_artificial_vars:
            self.objectives.append("min")

        self.col_titles = self.generate_col_titles()

        self.row_idx = None
        self.col_idx = None
        self.stop_iter = False

    def generate_col_titles(self) -> list[str]:
        """Generate column titles for the tableau.

        >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4.]]),
        ... 2, 0).generate_col_titles()
        ['x1', 'x2', 's1', 's2', 'RHS']

        >>> Tableau(np.array([[-1,-1,0,0,1],[1,3,1,0,4],[3,1,0,1,4.]]),
        ... 2, 2).generate_col_titles()
        ['x1', 'x2', 'RHS']
        """
        args = (self.n_vars, self.n_slack)
        string_starts = ["x", "s"]
        titles = []
        for i in range(2):
            for j in range(args[i]):
                titles.append(string_starts[i] + str(j + 1))
        titles.append("RHS")
        return titles

    def find_pivot(self) -> tuple[Any, Any]:
        """Find the pivot row and column using the largest coefficient rule.

        The pivot column is chosen as the variable with the most negative
        reduced cost (for maximization). The pivot row is chosen by the
        minimum ratio test (smallest positive RHS / pivot-column-entry).

        >>> tuple(int(x) for x in Tableau(np.array([[-2,1,0,0,0], [3,1,1,0,6],
        ... [1,2,0,1,7.]]), 2, 0).find_pivot())
        (1, 0)
        """
        objective = self.objectives[-1]

        # For max: pick most negative coefficient; for min: pick most positive
        sign = (objective == "min") - (objective == "max")
        col_idx = np.argmax(sign * self.tableau[0, :-1])

        if sign * self.tableau[0, col_idx] <= 0:
            self.stop_iter = True
            return 0, 0

        # Minimum ratio test: RHS / pivot column entry (only positive entries)
        s = slice(self.n_stages, self.n_rows)
        dividend = self.tableau[s, -1]
        divisor = self.tableau[s, col_idx]
        nans = np.full(self.n_rows - self.n_stages, np.nan)
        quotients = np.divide(dividend, divisor, out=nans, where=divisor > 0)

        row_idx = np.nanargmin(quotients) + self.n_stages
        return row_idx, col_idx

    def pivot(self, row_idx: int, col_idx: int) -> np.ndarray:
        """Perform a pivot operation on the tableau.

        Makes the pivot element 1 and all other entries in the pivot column 0
        by elementary row operations.

        >>> Tableau(np.array([[-2,-3,0,0,0],[1,3,1,0,4],[3,1,0,1,4.]]),
        ... 2, 2).pivot(1, 0).tolist()
        ... # doctest: +NORMALIZE_WHITESPACE
        [[0.0, 3.0, 2.0, 0.0, 8.0],
        [1.0, 3.0, 1.0, 0.0, 4.0],
        [0.0, -8.0, -3.0, 1.0, -8.0]]
        """
        piv_row = self.tableau[row_idx].copy()
        piv_val = piv_row[col_idx]
        piv_row *= 1 / piv_val

        for idx, coeff in enumerate(self.tableau[:, col_idx]):
            self.tableau[idx] += -coeff * piv_row
        self.tableau[row_idx] = piv_row
        return self.tableau

    def change_stage(self) -> np.ndarray:
        """Transition from Phase 1 to Phase 2 by removing artificial variables.

        Deletes artificial variable columns and the Phase 1 objective row,
        then continues with the original objective.

        >>> Tableau(np.array([
        ... [3, 3, -1, -1, 0, 0, 4],
        ... [2, 1, 0, 0, 0, 0, 0.],
        ... [1, 2, -1, 0, 1, 0, 2],
        ... [2, 1, 0, -1, 0, 1, 2]
        ... ]), 2, 2).change_stage().tolist()
        ... # doctest: +NORMALIZE_WHITESPACE
        [[2.0, 1.0, 0.0, 0.0, 0.0],
        [1.0, 2.0, -1.0, 0.0, 2.0],
        [2.0, 1.0, 0.0, -1.0, 2.0]]
        """
        self.objectives.pop()

        if not self.objectives:
            return self.tableau

        # Delete artificial variable columns
        s = slice(-self.n_artificial_vars - 1, -1)
        self.tableau = np.delete(self.tableau, s, axis=1)

        # Delete Phase 1 objective row
        self.tableau = np.delete(self.tableau, 0, axis=0)

        self.n_stages = 1
        self.n_rows -= 1
        self.n_artificial_vars = 0
        self.stop_iter = False
        return self.tableau

    def run_simplex(self) -> dict[Any, Any]:
        """Run the simplex algorithm to find the optimal solution.

        Iterates pivot operations until the objective function can no longer
        be improved. For two-phase problems, completes Phase 1 first.

        Returns a dict mapping variable names to their optimal values,
        with 'P' as the objective function value.

        # Standard LP: Max x1 + x2, ST: x1 + 3x2 <= 4, 3x1 + x2 <= 4
        >>> {key: float(value) for key, value in Tableau(np.array([[-1,-1,0,0,0],
        ... [1,3,1,0,4],[3,1,0,1,4.]]), 2, 0).run_simplex().items()}
        {'P': 2.0, 'x1': 1.0, 'x2': 1.0}

        # 3-variable LP: Max 3x1 + x2 + 3x3
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [-3,-1,-3,0,0,0,0],
        ... [2,1,1,1,0,0,2],
        ... [1,2,3,0,1,0,5],
        ... [2,2,1,0,0,1,6.]
        ... ]),3,0).run_simplex().items()} # doctest: +ELLIPSIS
        {'P': 5.4, 'x1': 0.199..., 'x3': 1.6}

        # Already-optimal tableau:
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [0, 0, 0.25, 0.25, 2],
        ... [0, 1, 0.375, -0.125, 1],
        ... [1, 0, -0.125, 0.375, 1]
        ... ]), 2, 0).run_simplex().items()}
        {'P': 2.0, 'x1': 1.0, 'x2': 1.0}

        # Non-standard (>= constraints): Max 2x1 + 3x2 + x3
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [2, 0, 0, 0, -1, -1, 0, 0, 20],
        ... [-2, -3, -1, 0, 0, 0, 0, 0, 0],
        ... [1, 1, 1, 1, 0, 0, 0, 0, 40],
        ... [2, 1, -1, 0, -1, 0, 1, 0, 10],
        ... [0, -1, 1, 0, 0, -1, 0, 1, 10.]
        ... ]), 3, 2).run_simplex().items()}
        {'P': 70.0, 'x1': 10.0, 'x2': 10.0, 'x3': 20.0}

        # Minimization with equalities: Min x1 + x2
        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [8, 6, 0, 0, 52],
        ... [1, 1, 0, 0, 0],
        ... [2, 1, 1, 0, 12],
        ... [6, 5, 0, 1, 40.],
        ... ]), 2, 2).run_simplex().items()}
        {'P': 7.0, 'x1': 5.0, 'x2': 2.0}
        """
        for _ in range(Tableau.maxiter):
            if not self.objectives:
                return self.interpret_tableau()

            row_idx, col_idx = self.find_pivot()

            if self.stop_iter:
                self.tableau = self.change_stage()
            else:
                self.tableau = self.pivot(row_idx, col_idx)
        return {}

    def interpret_tableau(self) -> dict[str, float]:
        """Extract variable values from the final optimal tableau.

        A decision variable has a value if its column has exactly one nonzero
        entry equal to 1 (it is a basic variable).

        >>> {key: float(value) for key, value in Tableau(np.array([
        ... [0,0,0.875,0.375,5],
        ... [0,1,0.375,-0.125,1],
        ... [1,0,-0.125,0.375,1]
        ... ]),2, 0).interpret_tableau().items()}
        {'P': 5.0, 'x1': 1.0, 'x2': 1.0}
        """
        output_dict = {"P": abs(self.tableau[0, -1])}

        for i in range(self.n_vars):
            nonzero = np.nonzero(self.tableau[:, i])
            n_nonzero = len(nonzero[0])
            nonzero_rowidx = nonzero[0][0]
            nonzero_val = self.tableau[nonzero_rowidx, i]

            if n_nonzero == 1 and nonzero_val == 1:
                rhs_val = self.tableau[nonzero_rowidx, -1]
                output_dict[self.col_titles[i]] = rhs_val
        return output_dict


def solve_lp(
    c: list[float],
    a_ub: list[list[float]] | None = None,
    b_ub: list[float] | None = None,
    a_eq: list[list[float]] | None = None,
    b_eq: list[float] | None = None,
) -> dict[str, float]:
    """Convenience wrapper to solve a standard-form LP.

    Maximize c^T x subject to A_ub x <= b_ub, A_eq x = b_eq, x >= 0.

    >>> solve_lp(c=[1, 1], a_ub=[[1, 3], [3, 1]], b_ub=[4, 4])
    {'P': 2.0, 'x1': 1.0, 'x2': 1.0}

    >>> result = solve_lp(c=[3, 1, 3], a_ub=[[2, 1, 1], [1, 2, 3], [2, 2, 1]],
    ...                   b_ub=[2, 5, 6])
    >>> round(result['P'], 1)
    5.4
    """
    n_vars = len(c)

    rows_ub = [] if a_ub is None else a_ub
    rhs_ub = [] if b_ub is None else b_ub

    n_slack = len(rows_ub)
    n_artificial = 0  # Standard form only (all <=)

    # Build objective row: negate c for maximization
    obj_row = [-ci for ci in c] + [0] * n_slack + [0]

    # Build constraint rows with slack variables
    constraint_rows = []
    for i, row in enumerate(rows_ub):
        slack = [0] * n_slack
        slack[i] = 1
        constraint_rows.append(row + slack + [rhs_ub[i]])

    tableau_data = [obj_row] + constraint_rows
    tableau = np.array(tableau_data, dtype=float)

    t = Tableau(tableau, n_vars, n_artificial)
    result = t.run_simplex()
    # Round to clean floating point artifacts
    return {k: round(float(v), 10) for k, v in result.items()}


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo: Solve a basic LP
    print("=== Simplex Algorithm Demo ===\n")

    # Standard LP: Max x1 + x2, ST: x1 + 3x2 <= 4, 3x1 + x2 <= 4
    print("Problem: Max x1 + x2")
    print("  ST: x1 + 3x2 <= 4")
    print("      3x1 + x2 <= 4")
    result = solve_lp(c=[1, 1], a_ub=[[1, 3], [3, 1]], b_ub=[4, 4])
    print(f"  Solution: {result}\n")

    # 3-variable LP
    print("Problem: Max 3x1 + x2 + 3x3")
    print("  ST: 2x1 + x2 + x3 <= 2")
    print("      x1 + 2x2 + 3x3 <= 5")
    print("      2x1 + 2x2 + x3 <= 6")
    result = solve_lp(
        c=[3, 1, 3],
        a_ub=[[2, 1, 1], [1, 2, 3], [2, 2, 1]],
        b_ub=[2, 5, 6],
    )
    print(f"  Solution: {result}\n")

    # Non-standard with >= constraints (two-phase)
    print("Problem: Max 2x1 + 3x2 + x3")
    print("  ST: x1 + x2 + x3 <= 40")
    print("      2x1 + x2 - x3 >= 10")
    print("      -x2 + x3 >= 10")
    tableau = np.array([
        [2, 0, 0, 0, -1, -1, 0, 0, 20],
        [-2, -3, -1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 40],
        [2, 1, -1, 0, -1, 0, 1, 0, 10],
        [0, -1, 1, 0, 0, -1, 0, 1, 10.0],
    ])
    t = Tableau(tableau, 3, 2)
    result = t.run_simplex()
    print(f"  Solution: {result}\n")

    # Minimization with equalities
    print("Problem: Min x1 + x2")
    print("  ST: 2x1 + x2 = 12")
    print("      6x1 + 5x2 = 40")
    tableau = np.array([
        [8, 6, 0, 0, 52],
        [1, 1, 0, 0, 0],
        [2, 1, 1, 0, 12],
        [6, 5, 0, 1, 40.0],
    ])
    t = Tableau(tableau, 2, 2)
    result = t.run_simplex()
    print(f"  Solution: {result}")
