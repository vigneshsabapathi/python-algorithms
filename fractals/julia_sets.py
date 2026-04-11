"""
Julia Sets — Quadratic Polynomial and Exponential Map Iteration

Draws Julia sets by iterating f(z) = z^2 + c (quadratic) or f(z) = e^z + c
(exponential) a fixed number of times, then checking whether |z_n| exceeds
an escape radius. Points that remain bounded approximate the Julia set.

Reference: https://en.wikipedia.org/wiki/Julia_set
Based on: https://github.com/TheAlgorithms/Python/blob/master/fractals/julia_sets.py

Doctests use only numpy (no matplotlib).
"""

import warnings
from collections.abc import Callable
from typing import Any

import numpy as np


# --- Classic parameters ---
c_cauliflower = 0.25 + 0.0j
c_polynomial_1 = -0.4 + 0.6j
c_polynomial_2 = -0.1 + 0.651j
c_exponential = -2.0
nb_iterations = 56
window_size = 2.0
nb_pixels = 666


def eval_exponential(c_parameter: complex, z_values: np.ndarray) -> np.ndarray:
    """
    Evaluate e^z + c.

    >>> float(eval_exponential(0, 0))
    1.0
    >>> bool(abs(eval_exponential(1, np.pi * 1.0j)) < 1e-15)
    True
    >>> bool(abs(eval_exponential(1.0j, 0) - 1 - 1.0j) < 1e-15)
    True
    """
    return np.exp(z_values) + c_parameter


def eval_quadratic_polynomial(
    c_parameter: complex, z_values: np.ndarray
) -> np.ndarray:
    """
    Evaluate z^2 + c.

    >>> eval_quadratic_polynomial(0, 2)
    4
    >>> eval_quadratic_polynomial(-1, 1)
    0
    >>> round(eval_quadratic_polynomial(1.0j, 0).imag)
    1
    >>> round(eval_quadratic_polynomial(1.0j, 0).real)
    0
    """
    return z_values * z_values + c_parameter


def prepare_grid(window_size: float, nb_pixels: int) -> np.ndarray:
    """
    Create an nb_pixels x nb_pixels grid of complex values with real and
    imaginary parts in [-window_size, window_size].

    >>> prepare_grid(1, 3)
    array([[-1.-1.j, -1.+0.j, -1.+1.j],
           [ 0.-1.j,  0.+0.j,  0.+1.j],
           [ 1.-1.j,  1.+0.j,  1.+1.j]])
    """
    x = np.linspace(-window_size, window_size, nb_pixels).reshape((nb_pixels, 1))
    y = np.linspace(-window_size, window_size, nb_pixels).reshape((1, nb_pixels))
    return x + 1.0j * y


def iterate_function(
    eval_function: Callable[[Any, np.ndarray], np.ndarray],
    function_params: Any,
    nb_iterations: int,
    z_0: np.ndarray,
    infinity: float | None = None,
) -> np.ndarray:
    """
    Iterate eval_function(params, z) exactly nb_iterations times starting
    from z_0.  Returns the final iterate array.

    >>> iterate_function(eval_quadratic_polynomial, 0, 3, np.array([0, 1, 2])).shape
    (3,)
    >>> complex(np.round(iterate_function(eval_quadratic_polynomial, 0, 3, np.array([0, 1, 2]))[0]))
    0j
    >>> complex(np.round(iterate_function(eval_quadratic_polynomial, 0, 3, np.array([0, 1, 2]))[1]))
    (1+0j)
    >>> complex(np.round(iterate_function(eval_quadratic_polynomial, 0, 3, np.array([0, 1, 2]))[2]))
    (256+0j)
    """
    z_n = z_0.astype("complex64")
    for _ in range(nb_iterations):
        z_n = eval_function(function_params, z_n)
        if infinity is not None:
            np.nan_to_num(z_n, copy=False, nan=infinity)
            z_n[abs(z_n) == np.inf] = infinity
    return z_n


def classify_points(
    c: complex,
    eval_fn: Callable = eval_quadratic_polynomial,
    grid_size: int = 10,
    win: float = 2.0,
    iterations: int = 20,
    escape_radius: float = 2.0,
) -> tuple[int, int]:
    """
    Count how many grid points escape vs remain bounded for a given c.
    Returns (escaped_count, bounded_count).

    >>> esc, bnd = classify_points(0.0 + 0.0j, grid_size=5, iterations=10)
    >>> esc >= 0 and bnd >= 0
    True
    >>> esc + bnd == 25
    True
    """
    z_0 = prepare_grid(win, grid_size)
    z_final = iterate_function(eval_fn, c, iterations, z_0, infinity=1.1 * escape_radius)
    escaped = int(np.sum(abs(z_final) >= escape_radius))
    bounded = grid_size * grid_size - escaped
    return escaped, bounded


def ignore_overflow_warnings() -> None:
    """
    Suppress overflow/invalid-value warnings from numpy iteration.

    >>> ignore_overflow_warnings()
    """
    for msg in (
        "overflow encountered in multiply",
        "invalid value encountered in multiply",
        "overflow encountered in absolute",
        "overflow encountered in exp",
    ):
        warnings.filterwarnings("ignore", category=RuntimeWarning, message=msg)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    ignore_overflow_warnings()

    # Demo: classify points for cauliflower Julia set
    print("=== Julia Sets Demo ===")
    for label, c_val in [
        ("Cauliflower (c=0.25)", c_cauliflower),
        ("Polynomial 1 (c=-0.4+0.6j)", c_polynomial_1),
        ("Polynomial 2 (c=-0.1+0.651j)", c_polynomial_2),
    ]:
        esc, bnd = classify_points(c_val, grid_size=50, iterations=30)
        total = esc + bnd
        print(f"{label}: {bnd}/{total} bounded ({100*bnd/total:.1f}%)")

    # Exponential map
    z_0 = prepare_grid(2.0, 50)
    z_final = iterate_function(eval_exponential, c_exponential, 12, z_0 + 2, infinity=1e10)
    bounded = int(np.sum(abs(z_final) < 10000))
    print(f"Exponential (c={c_exponential}): {bounded}/{50*50} bounded ({100*bounded/2500:.1f}%)")
