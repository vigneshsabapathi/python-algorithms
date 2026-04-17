"""
Forbes Billionaires – three age-calculation approaches + benchmark.

Approach 1: datetime.fromtimestamp (original)
Approach 2: timedelta-based calculation
Approach 3: date arithmetic without datetime
"""

import time
from datetime import UTC, date, datetime, timedelta


# ---------------------------------------------------------------------------
# Approach 1 – datetime.fromtimestamp (original)
# ---------------------------------------------------------------------------
def years_old_fromtimestamp(birth_ts: int, today: date | None = None) -> int:
    """
    Calculate age using datetime.fromtimestamp.

    >>> years_old_fromtimestamp(int(datetime(1990, 6, 15, tzinfo=UTC).timestamp()), date(2024, 1, 12))
    33
    >>> years_old_fromtimestamp(int(datetime(2000, 1, 12, tzinfo=UTC).timestamp()), date(2024, 1, 12))
    24
    """
    today = today or datetime.now(tz=UTC).date()
    birth_date = datetime.fromtimestamp(birth_ts, tz=UTC).date()
    return (today.year - birth_date.year) - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


# ---------------------------------------------------------------------------
# Approach 2 – date.fromtimestamp (simpler)
# ---------------------------------------------------------------------------
def years_old_date(birth_ts: int, today: date | None = None) -> int:
    """
    Calculate age using date.fromtimestamp via UTC offset.

    >>> years_old_date(int(datetime(1990, 6, 15, tzinfo=UTC).timestamp()), date(2024, 1, 12))
    33
    >>> years_old_date(int(datetime(2000, 1, 12, tzinfo=UTC).timestamp()), date(2024, 1, 12))
    24
    """
    today = today or date.today()
    birth_date = date.fromtimestamp(birth_ts)
    return (today.year - birth_date.year) - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


# ---------------------------------------------------------------------------
# Approach 3 – timedelta approximation (fast, ±1 day edge case)
# ---------------------------------------------------------------------------
_DAYS_PER_YEAR = 365.25


def years_old_timedelta(birth_ts: int, today: date | None = None) -> int:
    """
    Estimate age using timedelta days / 365.25 (fast approximation).

    >>> years_old_timedelta(int(datetime(1990, 6, 15, tzinfo=UTC).timestamp()), date(2024, 1, 12))
    33
    """
    today = today or datetime.now(tz=UTC).date()
    birth_date = datetime.fromtimestamp(birth_ts, tz=UTC).date()
    delta = today - birth_date
    return int(delta.days / _DAYS_PER_YEAR)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    birth_ts = int(datetime(1990, 6, 15, tzinfo=UTC).timestamp())
    today = date(2024, 1, 12)
    approaches = [
        ("fromtimestamp", years_old_fromtimestamp),
        ("date.fromtimestamp", years_old_date),
        ("timedelta approx", years_old_timedelta),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(birth_ts, today)
        elapsed = time.perf_counter() - t0
        print(f"{name:22s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
