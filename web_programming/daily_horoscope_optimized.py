"""
Daily Horoscope – three URL-building approaches + benchmark.

Approach 1: f-string (original)
Approach 2: str.format
Approach 3: urllib.parse.urlencode
"""

import time
from urllib.parse import urlencode

HOROSCOPE_BASE = (
    "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx"
)
ZODIAC_SIGNS = {
    1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
    5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio",
    9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces",
}


# ---------------------------------------------------------------------------
# Approach 1 – f-string
# ---------------------------------------------------------------------------
def build_url_fstring(day: str, sign: int) -> str:
    """
    Build horoscope URL using f-string.

    >>> build_url_fstring("today", 1)
    'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=1'
    """
    return HOROSCOPE_BASE.format(day=day) + f"?sign={sign}"


# ---------------------------------------------------------------------------
# Approach 2 – str.format
# ---------------------------------------------------------------------------
_URL_TEMPLATE = (
    "https://www.horoscope.com/us/horoscopes/general/"
    "horoscope-general-daily-{day}.aspx?sign={sign}"
)


def build_url_format(day: str, sign: int) -> str:
    """
    Build horoscope URL using str.format().

    >>> build_url_format("tomorrow", 5)
    'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-tomorrow.aspx?sign=5'
    """
    return _URL_TEMPLATE.format(day=day, sign=sign)


# ---------------------------------------------------------------------------
# Approach 3 – urlencode for query params
# ---------------------------------------------------------------------------
_BASE_TEMPLATE = (
    "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx"
)


def build_url_urlencode(day: str, sign: int) -> str:
    """
    Build horoscope URL using urllib.parse.urlencode for query string.

    >>> build_url_urlencode("yesterday", 12)
    'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-yesterday.aspx?sign=12'
    """
    base = _BASE_TEMPLATE.format(day=day)
    return f"{base}?{urlencode({'sign': sign})}"


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    approaches = [
        ("f-string", build_url_fstring),
        ("str.format", build_url_format),
        ("urlencode", build_url_urlencode),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn("today", 1)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
