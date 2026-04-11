"""
Koch Snowflake — Optimized Variants with Benchmark

Variant 1 (list_based): Original list-of-vectors approach
Variant 2 (numpy_batch): Batch numpy array processing
Variant 3 (generator_lazy): Lazy generator that yields points on demand
"""

import time

import numpy as np


# --- Variant 1: List-based (original) ---
def koch_list_based(steps: int) -> list[np.ndarray]:
    """
    Original list-of-vectors approach from TheAlgorithms.

    >>> len(koch_list_based(0))
    4
    >>> len(koch_list_based(3))
    193
    """
    vectors = [
        np.array([0.0, 0.0]),
        np.array([0.5, 0.8660254]),
        np.array([1.0, 0.0]),
        np.array([0.0, 0.0]),
    ]
    theta = np.radians(60)
    c, s = np.cos(theta), np.sin(theta)
    rot = np.array(((c, -s), (s, c)))

    for _ in range(steps):
        new = []
        for i in range(len(vectors) - 1):
            start, end = vectors[i], vectors[i + 1]
            diff = end - start
            new.append(start)
            new.append(start + diff / 3)
            new.append(start + diff / 3 + rot @ (diff / 3))
            new.append(start + diff * 2 / 3)
        new.append(vectors[-1])
        vectors = new
    return vectors


# --- Variant 2: Numpy batch (all points as a single array) ---
def koch_numpy_batch(steps: int) -> np.ndarray:
    """
    Process all segments simultaneously using numpy array operations.
    Returns an (N, 2) array of points.

    >>> koch_numpy_batch(0).shape
    (4, 2)
    >>> koch_numpy_batch(2).shape
    (49, 2)
    """
    pts = np.array([[0.0, 0.0], [0.5, 0.8660254], [1.0, 0.0], [0.0, 0.0]])
    theta = np.radians(60)
    c, s = np.cos(theta), np.sin(theta)

    for _ in range(steps):
        starts = pts[:-1]
        diffs = pts[1:] - starts
        third = diffs / 3

        # Rotate third vectors by 60 degrees
        rotated = np.column_stack([
            c * third[:, 0] - s * third[:, 1],
            s * third[:, 0] + c * third[:, 1],
        ])

        p1 = starts
        p2 = starts + third
        p3 = starts + third + rotated
        p4 = starts + 2 * third

        # Interleave: p1, p2, p3, p4 for each segment, then final point
        n = len(starts)
        new_pts = np.empty((4 * n + 1, 2))
        new_pts[0::4][:n] = p1
        new_pts[1::4][:n] = p2
        new_pts[2::4][:n] = p3
        new_pts[3::4][:n] = p4
        new_pts[-1] = pts[-1]
        pts = new_pts

    return pts


# --- Variant 3: Generator-based lazy evaluation ---
def koch_generator(steps: int):
    """
    Lazily yield (x, y) coordinate tuples without storing all at once.
    Memory-efficient for high step counts.

    >>> pts = list(koch_generator(1))
    >>> len(pts)
    13
    """
    theta = np.radians(60)
    c, s = np.cos(theta), np.sin(theta)

    initial = [
        (0.0, 0.0), (0.5, 0.8660254), (1.0, 0.0), (0.0, 0.0)
    ]

    def subdivide(segments, depth):
        if depth == 0:
            for seg in segments:
                yield seg[0]
            yield segments[-1][1]
            return

        def new_segs():
            for (sx, sy), (ex, ey) in segments:
                dx, dy = ex - sx, ey - sy
                t3x, t3y = dx / 3, dy / 3
                rx, ry = c * t3x - s * t3y, s * t3x + c * t3y
                p1 = (sx, sy)
                p2 = (sx + t3x, sy + t3y)
                p3 = (sx + t3x + rx, sy + t3y + ry)
                p4 = (sx + 2 * t3x, sy + 2 * t3y)
                p5 = (ex, ey)
                yield (p1, p2)
                yield (p2, p3)
                yield (p3, p4)
                yield (p4, p5)

        yield from subdivide(list(new_segs()), depth - 1)

    segments = [(initial[i], initial[i + 1]) for i in range(len(initial) - 1)]
    yield from subdivide(segments, steps)


def benchmark(max_steps: int = 5) -> None:
    """Run all three variants and compare timing."""
    print(f"Benchmark: Koch snowflake up to {max_steps} steps\n")

    for steps in range(max_steps + 1):
        times = {}

        start = time.perf_counter()
        r1 = koch_list_based(steps)
        times["list_based"] = time.perf_counter() - start

        start = time.perf_counter()
        r2 = koch_numpy_batch(steps)
        times["numpy_batch"] = time.perf_counter() - start

        start = time.perf_counter()
        r3 = list(koch_generator(steps))
        times["generator"] = time.perf_counter() - start

        fastest = min(times.values())
        n_pts = len(r1)
        print(f"  Step {steps} ({n_pts:>5} pts):", end="")
        for name, t in times.items():
            print(f"  {name}={t*1000:.2f}ms ({t/fastest:.1f}x)", end="")
        print()


if __name__ == "__main__":
    benchmark()
