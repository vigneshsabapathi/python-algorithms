"""
NASA Data – three URL-building and response-parsing approaches + benchmark.

Approach 1: requests.get params dict (original)
Approach 2: urllib.parse.urlencode
Approach 3: f-string with embedded params
"""

import time
from urllib.parse import urlencode

NASA_APOD_BASE = "https://api.nasa.gov/planetary/apod"
NASA_IMAGES_BASE = "https://images-api.nasa.gov/search"


# ---------------------------------------------------------------------------
# Approach 1 – dict params (passed to requests)
# ---------------------------------------------------------------------------
def build_apod_params(api_key: str) -> dict:
    """
    Build APOD request params as a dict.

    >>> p = build_apod_params("DEMO_KEY")
    >>> p["api_key"]
    'DEMO_KEY'
    """
    return {"api_key": api_key}


# ---------------------------------------------------------------------------
# Approach 2 – pre-built URL with urlencode
# ---------------------------------------------------------------------------
def build_apod_url_urlencode(api_key: str) -> str:
    """
    Build a fully-formed APOD URL using urlencode.

    >>> build_apod_url_urlencode("DEMO_KEY")
    'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
    """
    return f"{NASA_APOD_BASE}?{urlencode({'api_key': api_key})}"


# ---------------------------------------------------------------------------
# Approach 3 – f-string URL
# ---------------------------------------------------------------------------
def build_apod_url_fstring(api_key: str) -> str:
    """
    Build a fully-formed APOD URL using an f-string.

    >>> build_apod_url_fstring("MY_KEY")
    'https://api.nasa.gov/planetary/apod?api_key=MY_KEY'
    """
    return f"{NASA_APOD_BASE}?api_key={api_key}"


# ---------------------------------------------------------------------------
# Parse APOD response (offline helper)
# ---------------------------------------------------------------------------
def extract_image_filename(apod_url: str) -> str:
    """
    Extract the image filename from a NASA APOD image URL.

    >>> extract_image_filename("https://apod.nasa.gov/apod/image/2401/M31_1.jpg")
    'M31_1.jpg'
    >>> extract_image_filename("https://apod.nasa.gov/apod/image/2401/aurora.png")
    'aurora.png'
    """
    return apod_url.split("/")[-1]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    api_key = "DEMO_KEY"
    approaches = [
        ("dict params", build_apod_params),
        ("urlencode", build_apod_url_urlencode),
        ("f-string", build_apod_url_fstring),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(api_key)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
