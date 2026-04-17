"""
CO2 Emission – three implementation approaches and benchmark.

Approach 1: requests (synchronous, standard library-friendly)
Approach 2: httpx (modern sync client, HTTP/2 support)
Approach 3: Parse and filter cached response offline (pure, no network)
"""

import json
import time
from datetime import date, datetime, timezone


# ---------------------------------------------------------------------------
# Approach 1 – requests (standard)
# ---------------------------------------------------------------------------
def fetch_from_to_requests(start: date, end: date) -> list:
    """Use the requests library to fetch emission data."""
    import requests

    url = f"https://api.carbonintensity.org.uk/intensity/{start}/{end}"
    return requests.get(url, timeout=10).json()["data"]


# ---------------------------------------------------------------------------
# Approach 2 – httpx (modern HTTP client)
# ---------------------------------------------------------------------------
def fetch_from_to_httpx(start: date, end: date) -> list:
    """Use httpx for automatic HTTP/2 and connection pooling."""
    import httpx

    url = f"https://api.carbonintensity.org.uk/intensity/{start}/{end}"
    return httpx.get(url, timeout=10).json()["data"]


# ---------------------------------------------------------------------------
# Approach 3 – offline: filter a pre-loaded data list
# ---------------------------------------------------------------------------
def filter_by_date_range(data: list, start: date, end: date) -> list:
    """
    Filter a pre-loaded list of emission dicts to a date range (offline).

    Each item is expected to have 'from' and 'to' ISO-8601 strings.

    >>> sample = [
    ...     {"from": "2020-10-01T00:00Z", "to": "2020-10-01T00:30Z", "intensity": {"actual": 100}},
    ...     {"from": "2020-10-02T00:00Z", "to": "2020-10-02T00:30Z", "intensity": {"actual": 120}},
    ...     {"from": "2020-10-04T00:00Z", "to": "2020-10-04T00:30Z", "intensity": {"actual": 200}},
    ... ]
    >>> result = filter_by_date_range(sample, date(2020, 10, 1), date(2020, 10, 3))
    >>> len(result)
    2
    >>> result[0]["intensity"]["actual"]
    100
    """
    start_dt = datetime(start.year, start.month, start.day, tzinfo=timezone.utc)
    end_dt = datetime(end.year, end.month, end.day, tzinfo=timezone.utc)
    filtered = []
    for item in data:
        item_dt = datetime.fromisoformat(item["from"].replace("Z", "+00:00"))
        if start_dt <= item_dt < end_dt:
            filtered.append(item)
    return filtered


# ---------------------------------------------------------------------------
# Benchmark (offline only – no network calls)
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Benchmark the offline filter_by_date_range function."""
    sample_data = [
        {
            "from": f"2020-10-{day:02d}T00:00Z",
            "to": f"2020-10-{day:02d}T00:30Z",
            "intensity": {"actual": day * 10},
        }
        for day in range(1, 32)
    ]
    start = date(2020, 10, 1)
    end = date(2020, 10, 15)

    runs = 10_000
    t0 = time.perf_counter()
    for _ in range(runs):
        filter_by_date_range(sample_data, start, end)
    elapsed = time.perf_counter() - t0
    print(f"filter_by_date_range: {runs} runs in {elapsed:.4f}s "
          f"({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
