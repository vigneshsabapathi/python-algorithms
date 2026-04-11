"""
Fuzzy set operations — triangular membership functions with union,
intersection, complement, and membership queries.

A triangular fuzzy set is defined by three points (left, peak, right)
on the real line.  The membership function rises linearly from 0 at the
left boundary to 1 at the peak, then falls linearly back to 0 at the
right boundary.

Reference: https://en.wikipedia.org/wiki/Fuzzy_set
Source:     https://github.com/TheAlgorithms/Python/blob/master/fuzzy_logic/fuzzy_operations.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FuzzySet:
    """
    Triangular fuzzy set with support for core fuzzy-logic operations.

    Attributes:
        name:           Human-readable label for the set.
        left_boundary:  x-value where membership begins rising from 0.
        peak:           x-value where membership equals 1.
        right_boundary: x-value where membership falls back to 0.

    >>> a = FuzzySet("A", 0, 0.5, 1)
    >>> a
    FuzzySet(name='A', left_boundary=0, peak=0.5, right_boundary=1)
    >>> str(a)
    'A: [0, 0.5, 1]'

    >>> b = FuzzySet("B", 0.2, 0.7, 1)
    >>> b
    FuzzySet(name='B', left_boundary=0.2, peak=0.7, right_boundary=1)

    # Complement
    >>> a.complement()
    FuzzySet(name='NOT A', left_boundary=0, peak=0.5, right_boundary=1)
    >>> b.complement()
    FuzzySet(name='NOT B', left_boundary=0, peak=0.3, right_boundary=0.8)

    # Intersection — element-wise min of membership values
    >>> a.intersection(b)
    FuzzySet(name='A AND B', left_boundary=0.2, peak=0.5, right_boundary=1)

    # Union — element-wise max of membership values
    >>> a.union(b)
    FuzzySet(name='A OR B', left_boundary=0, peak=0.7, right_boundary=1)

    # Membership queries
    >>> a.membership(0.25)
    0.5
    >>> a.membership(0.75)
    0.5
    >>> a.membership(0.0)
    0.0
    >>> a.membership(1.0)
    0.0
    """

    name: str
    left_boundary: float
    peak: float
    right_boundary: float

    def __post_init__(self) -> None:
        """
        Validate that the triangular parameters are ordered correctly.

        >>> FuzzySet("bad", 0.5, 0.3, 1.0)
        Traceback (most recent call last):
            ...
        ValueError: Require left_boundary <= peak <= right_boundary, got 0.5, 0.3, 1.0
        """
        if not (self.left_boundary <= self.peak <= self.right_boundary):
            raise ValueError(
                f"Require left_boundary <= peak <= right_boundary, "
                f"got {self.left_boundary}, {self.peak}, {self.right_boundary}"
            )

    def __str__(self) -> str:
        """
        >>> str(FuzzySet("X", 0.1, 0.2, 0.3))
        'X: [0.1, 0.2, 0.3]'
        """
        return f"{self.name}: [{self.left_boundary}, {self.peak}, {self.right_boundary}]"

    # ------------------------------------------------------------------
    # Core fuzzy operations
    # ------------------------------------------------------------------

    def membership(self, x: float) -> float:
        """
        Calculate the degree of membership for value *x* in [0, 1].

        The triangular membership function:
        - 0                                 if x <= left  or  x >= right
        - (x - left) / (peak - left)        if left < x <= peak
        - (right - x) / (right - peak)      if peak < x < right

        >>> FuzzySet("A", 0, 0.5, 1).membership(0.1)
        0.2
        >>> FuzzySet("B", 0.2, 0.7, 1).membership(0.6)
        0.8
        >>> FuzzySet("C", 0.0, 0.5, 1.0).membership(0.5)
        1.0
        >>> FuzzySet("D", 0.0, 0.5, 1.0).membership(-0.1)
        0.0
        >>> FuzzySet("E", 0.0, 0.5, 1.0).membership(1.5)
        0.0
        """
        if x <= self.left_boundary or x >= self.right_boundary:
            return 0.0
        if x <= self.peak:
            # Rising edge
            denom = self.peak - self.left_boundary
            return (x - self.left_boundary) / denom if denom != 0 else 1.0
        # Falling edge
        denom = self.right_boundary - self.peak
        return (self.right_boundary - x) / denom if denom != 0 else 1.0

    def complement(self) -> FuzzySet:
        """
        Fuzzy complement (negation): membership_complement(x) = 1 - membership(x).

        For a triangular set (left, peak, right) the complement is the
        triangular set (1 - right, 1 - peak, 1 - left) reflected about x = 0.5.

        >>> FuzzySet("A", 0.1, 0.2, 0.3).complement()
        FuzzySet(name='NOT A', left_boundary=0.7, peak=0.8, right_boundary=0.9)
        """
        return FuzzySet(
            f"NOT {self.name}",
            round(1 - self.right_boundary, 10),
            round(1 - self.peak, 10),
            round(1 - self.left_boundary, 10),
        )

    def intersection(self, other: FuzzySet) -> FuzzySet:
        """
        Fuzzy intersection (AND): membership = min(mu_A(x), mu_B(x)).

        Approximated for triangular sets with clamping to maintain
        left <= peak <= right invariant.

        >>> FuzzySet("A", 0.1, 0.2, 0.3).intersection(FuzzySet("B", 0.15, 0.25, 0.35))
        FuzzySet(name='A AND B', left_boundary=0.15, peak=0.2, right_boundary=0.35)
        >>> FuzzySet("A", 0, 25, 50).intersection(FuzzySet("B", 30, 50, 70))
        FuzzySet(name='A AND B', left_boundary=30, peak=40.0, right_boundary=70)
        """
        left = max(self.left_boundary, other.left_boundary)
        right = max(self.right_boundary, other.right_boundary)
        # Use the overlap midpoint as the approximate peak, clamped
        peak = min(self.peak, other.peak)
        peak = max(peak, left)   # ensure peak >= left
        peak = min(peak, right)  # ensure peak <= right
        # If peak ended up clamped, use midpoint of overlap region
        if peak == left and left > min(self.peak, other.peak):
            peak = (left + min(self.right_boundary, other.right_boundary)) / 2
            peak = max(peak, left)
            peak = min(peak, right)
        return FuzzySet(
            f"{self.name} AND {other.name}",
            left,
            peak,
            right,
        )

    def union(self, other: FuzzySet) -> FuzzySet:
        """
        Fuzzy union (OR): membership = max(mu_A(x), mu_B(x)).

        Approximated for triangular sets as:
            left  = min(left_A,  left_B)
            peak  = max(peak_A,  peak_B)       -- tallest peak
            right = max(right_A, right_B)

        >>> FuzzySet("A", 0.1, 0.2, 0.3).union(FuzzySet("B", 0.15, 0.25, 0.35))
        FuzzySet(name='A OR B', left_boundary=0.1, peak=0.25, right_boundary=0.35)
        """
        return FuzzySet(
            f"{self.name} OR {other.name}",
            min(self.left_boundary, other.left_boundary),
            max(self.peak, other.peak),
            max(self.right_boundary, other.right_boundary),
        )

    def alpha_cut(self, alpha: float) -> tuple[float, float] | None:
        """
        Return the interval [x_low, x_high] where membership >= alpha.

        Returns None if no x satisfies the cut (alpha > 1 or alpha <= 0).

        >>> FuzzySet("A", 0, 0.5, 1).alpha_cut(0.5)
        (0.25, 0.75)
        >>> FuzzySet("A", 0, 0.5, 1).alpha_cut(1.0)
        (0.5, 0.5)
        >>> FuzzySet("A", 0, 0.5, 1).alpha_cut(0.0) is None
        True
        >>> FuzzySet("A", 0, 0.5, 1).alpha_cut(1.5) is None
        True
        """
        if alpha <= 0 or alpha > 1:
            return None
        x_low = self.left_boundary + alpha * (self.peak - self.left_boundary)
        x_high = self.right_boundary - alpha * (self.right_boundary - self.peak)
        return (round(x_low, 10), round(x_high, 10))

    def is_normal(self) -> bool:
        """
        A fuzzy set is normal if its peak membership equals 1, which is
        always true for a well-formed triangular set where left < peak < right.

        >>> FuzzySet("A", 0, 0.5, 1).is_normal()
        True
        >>> FuzzySet("P", 0.3, 0.3, 0.3).is_normal()
        False
        """
        return self.left_boundary < self.peak < self.right_boundary

    def centroid(self, n_points: int = 1000) -> float:
        """
        Defuzzify via the centroid (center-of-gravity) method.

        Numerically integrates: sum(x * mu(x)) / sum(mu(x))
        over [left_boundary, right_boundary].

        >>> round(FuzzySet("A", 0, 0.5, 1).centroid(), 4)
        0.5
        >>> round(FuzzySet("B", 0.2, 0.7, 1).centroid(), 4)
        0.6333
        """
        if self.left_boundary == self.right_boundary:
            return self.peak
        step = (self.right_boundary - self.left_boundary) / n_points
        numerator = 0.0
        denominator = 0.0
        x = self.left_boundary
        for _ in range(n_points + 1):
            mu = self.membership(x)
            numerator += x * mu
            denominator += mu
            x += step
        return numerator / denominator if denominator != 0 else self.peak


if __name__ == "__main__":
    import doctest

    doctest.testmod()
