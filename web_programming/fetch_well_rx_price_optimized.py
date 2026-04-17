"""
WellRx Price – three URL-building approaches + offline parsing benchmark.

Approach 1: str.format (original)
Approach 2: f-string
Approach 3: urllib.parse.urljoin
"""

import time
from urllib.parse import quote, urljoin

WELLRX_BASE = "https://www.wellrx.com/prescriptions/"
WELLRX_TEMPLATE = "https://www.wellrx.com/prescriptions/{drug}/{zip}/?freshSearch=true"


# ---------------------------------------------------------------------------
# Approach 1 – str.format (original)
# ---------------------------------------------------------------------------
def build_url_format(drug_name: str, zip_code: str) -> str:
    """
    Build WellRx URL using str.format.

    >>> build_url_format("eliquis", "30303")
    'https://www.wellrx.com/prescriptions/eliquis/30303/?freshSearch=true'
    """
    return WELLRX_TEMPLATE.format(drug=drug_name, zip=zip_code)


# ---------------------------------------------------------------------------
# Approach 2 – f-string
# ---------------------------------------------------------------------------
def build_url_fstring(drug_name: str, zip_code: str) -> str:
    """
    Build WellRx URL using an f-string.

    >>> build_url_fstring("lipitor", "10001")
    'https://www.wellrx.com/prescriptions/lipitor/10001/?freshSearch=true'
    """
    return f"https://www.wellrx.com/prescriptions/{drug_name}/{zip_code}/?freshSearch=true"


# ---------------------------------------------------------------------------
# Approach 3 – urljoin
# ---------------------------------------------------------------------------
def build_url_urljoin(drug_name: str, zip_code: str) -> str:
    """
    Build WellRx URL using urljoin with URL-encoded parts.

    >>> build_url_urljoin("metformin", "90210")
    'https://www.wellrx.com/prescriptions/metformin/90210/?freshSearch=true'
    """
    path = f"{quote(drug_name)}/{quote(zip_code)}/?freshSearch=true"
    return urljoin(WELLRX_BASE, path)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    approaches = [
        ("str.format", build_url_format),
        ("f-string", build_url_fstring),
        ("urljoin", build_url_urljoin),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn("eliquis", "30303")
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
