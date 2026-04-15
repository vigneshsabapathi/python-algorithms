"""
Gamma function Γ(n): extends factorial to reals. Γ(n) = (n-1)! for positive integers.

Computed via numerical integration of ∫₀^∞ t^(x-1) e^(-t) dt.

>>> round(gamma(5), 3)
24.0
>>> round(gamma(1), 3)
1.0
>>> round(gamma(0.5), 3)  # sqrt(pi)
1.772
"""

import math
from scipy import integrate  # type: ignore


def gamma(num: float) -> float:
    """Γ(num) via integration.

    >>> round(gamma(4), 3)
    6.0
    """
    if num <= 0:
        raise ValueError("gamma requires positive input")
    return integrate.quad(lambda t: t ** (num - 1) * math.exp(-t), 0, math.inf)[0]


def gamma_builtin(num: float) -> float:
    """Via math.gamma."""
    return math.gamma(num)


if __name__ == "__main__":
    try:
        import doctest

        doctest.testmod()
    except Exception as e:  # scipy might not be installed
        print(f"skipping doctest: {e}")
    print(math.gamma(5))
