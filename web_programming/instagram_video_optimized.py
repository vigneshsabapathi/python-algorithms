"""
Instagram Video – three filename-generation approaches + benchmark.

Approach 1: datetime strftime f-string (original)
Approach 2: time.strftime
Approach 3: ISO format + replace
"""

import time
from datetime import UTC, datetime


# ---------------------------------------------------------------------------
# Approach 1 – datetime strftime via f-string format spec (original)
# ---------------------------------------------------------------------------
def generate_filename_fstring() -> str:
    """
    Generate a timestamp-based .mp4 filename using datetime f-string format.

    >>> name = generate_filename_fstring()
    >>> name.endswith(".mp4")
    True
    >>> len(name) == len("2024-01-01_12-00-00.mp4")
    True
    """
    return f"{datetime.now(tz=UTC).astimezone():%Y-%m-%d_%H-%M-%S}.mp4"


# ---------------------------------------------------------------------------
# Approach 2 – time.strftime
# ---------------------------------------------------------------------------
def generate_filename_time() -> str:
    """
    Generate a timestamp-based .mp4 filename using time.strftime.

    >>> name = generate_filename_time()
    >>> name.endswith(".mp4")
    True
    """
    import time as _time
    return _time.strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"


# ---------------------------------------------------------------------------
# Approach 3 – isoformat + replace
# ---------------------------------------------------------------------------
def generate_filename_iso() -> str:
    """
    Generate a .mp4 filename from ISO format with character replacement.

    >>> name = generate_filename_iso()
    >>> name.endswith(".mp4")
    True
    """
    ts = datetime.now(tz=UTC).astimezone().isoformat(timespec="seconds")
    safe = ts[:19].replace(":", "-").replace("T", "_")
    return f"{safe}.mp4"


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 100_000) -> None:
    approaches = [
        ("datetime f-string", generate_filename_fstring),
        ("time.strftime", generate_filename_time),
        ("isoformat+replace", generate_filename_iso),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn()
        elapsed = time.perf_counter() - t0
        print(f"{name:22s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
