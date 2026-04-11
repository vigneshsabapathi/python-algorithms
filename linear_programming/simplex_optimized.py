"""
Simplex Algorithm Variants & Benchmark

Compares different pivoting rules for the simplex method:
  1. Largest Coefficient (Dantzig's rule) - standard, picks most negative reduced cost
  2. Bland's Rule - prevents cycling by always picking smallest index
  3. Steepest Edge Approximation - normalizes by pivot column norm

Also benchmarks against scipy.optimize.linprog (revised simplex / HiGHS).
"""

import time
from typing import Any

import numpy as np


# ---------------------------------------------------------------------------
# Variant 1: Largest Coefficient Rule (Dantzig's Rule) -- the standard rule
# ---------------------------------------------------------------------------

def simplex_largest_coefficient(
    c: list[float],
    A_ub: list[list[float]],
    b_ub: list[float],
) -> dict[str, Any]:
    """
    Solve Max c^T x, s.t. A_ub x <= b_ub, x >= 0 using the largest
    coefficient (most negative reduced cost) pivoting rule.

    This is the classic Dantzig pivot rule: enter the variable whose
    reduced cost is most negative, giving the steepest per-unit improvement.

    >>> r = simplex_largest_coefficient([1, 1], [[1, 3], [3, 1]], [4, 4])
    >>> r['P'], r['x1'], r['x2']
    (2.0, 1.0, 1.0)

    >>> r = simplex_largest_coefficient([5, 4, 3],
    ...     [[6, 4, 2], [3, 3, 5]], [240, 270])
    >>> round(r['P'], 4)
    265.7143
    """
    n_vars = len(c)
    n_constraints = len(b_ub)

    # Build tableau: objective row + constraint rows with slack
    # Columns: x1..xn | s1..sm | RHS
    n_cols = n_vars + n_constraints + 1
    tableau = np.zeros((n_constraints + 1, n_cols))

    # Objective row (negate for maximization)
    tableau[0, :n_vars] = [-ci for ci in c]

    # Constraint rows
    for i in range(n_constraints):
        tableau[i + 1, :n_vars] = A_ub[i]
        tableau[i + 1, n_vars + i] = 1.0  # slack variable
        tableau[i + 1, -1] = b_ub[i]

    pivots = 0
    max_iter = 1000

    for _ in range(max_iter):
        # Find entering variable: most negative in objective row
        obj_row = tableau[0, :-1]
        col_idx = np.argmin(obj_row)

        if obj_row[col_idx] >= -1e-10:
            break  # Optimal

        # Minimum ratio test for leaving variable
        col = tableau[1:, col_idx]
        rhs = tableau[1:, -1]

        ratios = np.full(n_constraints, np.inf)
        positive = col > 1e-10
        ratios[positive] = rhs[positive] / col[positive]

        if np.all(np.isinf(ratios)):
            return {"status": "unbounded"}

        row_idx = np.argmin(ratios) + 1

        # Pivot
        pivot_val = tableau[row_idx, col_idx]
        tableau[row_idx] /= pivot_val
        for i in range(len(tableau)):
            if i != row_idx:
                tableau[i] -= tableau[i, col_idx] * tableau[row_idx]
        pivots += 1

    # Extract solution
    result: dict[str, Any] = {"P": round(float(tableau[0, -1]), 10)}
    for j in range(n_vars):
        col = tableau[:, j]
        nonzero = np.nonzero(col)[0]
        if len(nonzero) == 1 and abs(col[nonzero[0]] - 1.0) < 1e-10:
            result[f"x{j + 1}"] = round(float(tableau[nonzero[0], -1]), 10)
    result["pivots"] = pivots
    return result


# ---------------------------------------------------------------------------
# Variant 2: Bland's Rule -- guarantees no cycling
# ---------------------------------------------------------------------------

def simplex_bland(
    c: list[float],
    A_ub: list[list[float]],
    b_ub: list[float],
) -> dict[str, Any]:
    """
    Solve Max c^T x, s.t. A_ub x <= b_ub, x >= 0 using Bland's rule.

    Bland's rule: among all variables with negative reduced cost, pick the one
    with the smallest index. This guarantees finite termination (no cycling)
    at the cost of potentially more pivot steps.

    >>> r = simplex_bland([1, 1], [[1, 3], [3, 1]], [4, 4])
    >>> r['P'], r['x1'], r['x2']
    (2.0, 1.0, 1.0)

    >>> r = simplex_bland([5, 4, 3], [[6, 4, 2], [3, 3, 5]], [240, 270])
    >>> round(r['P'], 4)
    265.7143
    """
    n_vars = len(c)
    n_constraints = len(b_ub)
    n_cols = n_vars + n_constraints + 1
    tableau = np.zeros((n_constraints + 1, n_cols))

    tableau[0, :n_vars] = [-ci for ci in c]
    for i in range(n_constraints):
        tableau[i + 1, :n_vars] = A_ub[i]
        tableau[i + 1, n_vars + i] = 1.0
        tableau[i + 1, -1] = b_ub[i]

    pivots = 0
    max_iter = 1000

    for _ in range(max_iter):
        # Bland's rule: pick SMALLEST index with negative reduced cost
        obj_row = tableau[0, :-1]
        col_idx = None
        for j in range(len(obj_row)):
            if obj_row[j] < -1e-10:
                col_idx = j
                break

        if col_idx is None:
            break  # Optimal

        # Minimum ratio test (also use smallest index for ties = Bland)
        col = tableau[1:, col_idx]
        rhs = tableau[1:, -1]

        min_ratio = np.inf
        row_idx = -1
        for i in range(n_constraints):
            if col[i] > 1e-10:
                ratio = rhs[i] / col[i]
                if ratio < min_ratio - 1e-10:
                    min_ratio = ratio
                    row_idx = i + 1

        if row_idx == -1:
            return {"status": "unbounded"}

        # Pivot
        pivot_val = tableau[row_idx, col_idx]
        tableau[row_idx] /= pivot_val
        for i in range(len(tableau)):
            if i != row_idx:
                tableau[i] -= tableau[i, col_idx] * tableau[row_idx]
        pivots += 1

    result: dict[str, Any] = {"P": round(float(tableau[0, -1]), 10)}
    for j in range(n_vars):
        col = tableau[:, j]
        nonzero = np.nonzero(col)[0]
        if len(nonzero) == 1 and abs(col[nonzero[0]] - 1.0) < 1e-10:
            result[f"x{j + 1}"] = round(float(tableau[nonzero[0], -1]), 10)
    result["pivots"] = pivots
    return result


# ---------------------------------------------------------------------------
# Variant 3: Steepest Edge Approximation
# ---------------------------------------------------------------------------

def simplex_steepest_edge(
    c: list[float],
    A_ub: list[list[float]],
    b_ub: list[float],
) -> dict[str, Any]:
    """
    Solve Max c^T x, s.t. A_ub x <= b_ub, x >= 0 using a steepest-edge
    approximation pivoting rule.

    Instead of picking the most negative reduced cost, picks the variable
    whose reduced cost divided by the column's Euclidean norm is most
    negative. This approximates the direction of steepest improvement
    in the objective function and often reduces pivot count.

    >>> r = simplex_steepest_edge([1, 1], [[1, 3], [3, 1]], [4, 4])
    >>> r['P'], r['x1'], r['x2']
    (2.0, 1.0, 1.0)

    >>> r = simplex_steepest_edge([5, 4, 3],
    ...     [[6, 4, 2], [3, 3, 5]], [240, 270])
    >>> round(r['P'], 4)
    265.7143
    """
    n_vars = len(c)
    n_constraints = len(b_ub)
    n_cols = n_vars + n_constraints + 1
    tableau = np.zeros((n_constraints + 1, n_cols))

    tableau[0, :n_vars] = [-ci for ci in c]
    for i in range(n_constraints):
        tableau[i + 1, :n_vars] = A_ub[i]
        tableau[i + 1, n_vars + i] = 1.0
        tableau[i + 1, -1] = b_ub[i]

    pivots = 0
    max_iter = 1000

    for _ in range(max_iter):
        obj_row = tableau[0, :-1]

        # Steepest edge: normalize reduced cost by column norm
        negative_mask = obj_row < -1e-10
        if not np.any(negative_mask):
            break  # Optimal

        scores = np.full(len(obj_row), np.inf)
        for j in range(len(obj_row)):
            if negative_mask[j]:
                col_norm = np.linalg.norm(tableau[1:, j])
                if col_norm > 1e-10:
                    scores[j] = obj_row[j] / col_norm  # More negative = better

        col_idx = int(np.argmin(scores))

        # Minimum ratio test
        col = tableau[1:, col_idx]
        rhs = tableau[1:, -1]

        ratios = np.full(n_constraints, np.inf)
        positive = col > 1e-10
        ratios[positive] = rhs[positive] / col[positive]

        if np.all(np.isinf(ratios)):
            return {"status": "unbounded"}

        row_idx = int(np.argmin(ratios)) + 1

        # Pivot
        pivot_val = tableau[row_idx, col_idx]
        tableau[row_idx] /= pivot_val
        for i in range(len(tableau)):
            if i != row_idx:
                tableau[i] -= tableau[i, col_idx] * tableau[row_idx]
        pivots += 1

    result: dict[str, Any] = {"P": round(float(tableau[0, -1]), 10)}
    for j in range(n_vars):
        col = tableau[:, j]
        nonzero = np.nonzero(col)[0]
        if len(nonzero) == 1 and abs(col[nonzero[0]] - 1.0) < 1e-10:
            result[f"x{j + 1}"] = round(float(tableau[nonzero[0], -1]), 10)
    result["pivots"] = pivots
    return result


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    """Compare all three pivot rules + scipy on various problem sizes."""
    from scipy.optimize import linprog

    problems = [
        {
            "name": "Small 2-var",
            "c": [1, 1],
            "A_ub": [[1, 3], [3, 1]],
            "b_ub": [4, 4],
        },
        {
            "name": "Medium 3-var",
            "c": [5, 4, 3],
            "A_ub": [[6, 4, 2], [3, 3, 5]],
            "b_ub": [240, 270],
        },
    ]

    # Generate a larger random problem
    rng = np.random.default_rng(42)
    n, m = 20, 40  # 20 variables, 40 constraints
    A_large = rng.uniform(0, 10, size=(m, n)).tolist()
    b_large = rng.uniform(50, 200, size=m).tolist()
    c_large = rng.uniform(1, 10, size=n).tolist()
    problems.append({
        "name": f"Random {n}-var {m}-constraint",
        "c": c_large,
        "A_ub": A_large,
        "b_ub": b_large,
    })

    # Even larger problem
    n2, m2 = 50, 100
    A_xl = rng.uniform(0, 10, size=(m2, n2)).tolist()
    b_xl = rng.uniform(50, 200, size=m2).tolist()
    c_xl = rng.uniform(1, 10, size=n2).tolist()
    problems.append({
        "name": f"Large {n2}-var {m2}-constraint",
        "c": c_xl,
        "A_ub": A_xl,
        "b_ub": b_xl,
    })

    solvers = [
        ("Largest Coefficient", simplex_largest_coefficient),
        ("Bland's Rule", simplex_bland),
        ("Steepest Edge", simplex_steepest_edge),
    ]

    print("=" * 78)
    print(f"{'Simplex Pivot Rule Benchmark':^78}")
    print("=" * 78)

    for prob in problems:
        print(f"\n--- {prob['name']} ---")
        print(f"{'Method':<25} {'Objective':>12} {'Pivots':>8} {'Time (us)':>12}")
        print("-" * 60)

        for name, solver in solvers:
            # Warm up
            solver(prob["c"], prob["A_ub"], prob["b_ub"])

            # Timed run
            n_runs = 100
            start = time.perf_counter()
            for _ in range(n_runs):
                result = solver(prob["c"], prob["A_ub"], prob["b_ub"])
            elapsed = (time.perf_counter() - start) / n_runs * 1e6

            obj = result.get("P", "N/A")
            pivots = result.get("pivots", "?")
            print(f"{name:<25} {obj:>12.4f} {pivots:>8} {elapsed:>12.1f}")

        # scipy comparison
        # scipy minimizes, so negate c for maximization
        c_neg = [-ci for ci in prob["c"]]
        A_np = np.array(prob["A_ub"])
        b_np = np.array(prob["b_ub"])

        # Warm up
        linprog(c_neg, A_ub=A_np, b_ub=b_np, method="highs")

        n_runs_scipy = 100
        start = time.perf_counter()
        for _ in range(n_runs_scipy):
            res = linprog(c_neg, A_ub=A_np, b_ub=b_np, method="highs")
        elapsed = (time.perf_counter() - start) / n_runs_scipy * 1e6
        obj_scipy = -res.fun if res.success else float("nan")
        print(f"{'scipy (HiGHS)':<25} {obj_scipy:>12.4f} {'N/A':>8} {elapsed:>12.1f}")

    print("\n" + "=" * 78)
    print("Notes:")
    print("  - Largest Coefficient: Classic Dantzig rule, fast but may cycle")
    print("  - Bland's Rule: Anti-cycling guarantee, may need more pivots")
    print("  - Steepest Edge: Better pivot selection, fewer pivots on large problems")
    print("  - scipy HiGHS: Production-grade interior point / simplex solver")
    print("=" * 78)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
