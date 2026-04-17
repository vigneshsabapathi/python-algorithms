"""
Fetch Anime – three URL-building and list-filtering approaches + benchmark.

Approach 1: f-string base URL concat (original)
Approach 2: urllib.parse.urljoin
Approach 3: tag-safe NavigableString filter using isinstance
"""

import time
from urllib.parse import urljoin

BASE_URL = "https://ww7.gogoanime2.org"


# ---------------------------------------------------------------------------
# Approach 1 – f-string concat (original)
# ---------------------------------------------------------------------------
def build_search_url_fstring(base: str, keyword: str) -> str:
    """
    Build a gogoanime search URL using f-string.

    >>> build_search_url_fstring("https://ww7.gogoanime2.org", "demon_slayer")
    'https://ww7.gogoanime2.org/search?keyword=demon_slayer'
    """
    return f"{base}/search?keyword={keyword}"


# ---------------------------------------------------------------------------
# Approach 2 – urljoin
# ---------------------------------------------------------------------------
def build_search_url_urljoin(base: str, keyword: str) -> str:
    """
    Build a gogoanime search URL using urljoin.

    >>> build_search_url_urljoin("https://ww7.gogoanime2.org", "naruto")
    'https://ww7.gogoanime2.org/search?keyword=naruto'
    """
    from urllib.parse import urlencode

    return urljoin(base, f"/search?{urlencode({'keyword': keyword})}")


# ---------------------------------------------------------------------------
# Approach 3 – episode URL transform
# ---------------------------------------------------------------------------
def transform_embed_to_playlist(episode_url: str) -> str:
    """
    Convert an embed episode URL to its .m3u8 playlist download URL.

    >>> transform_embed_to_playlist("https://gogoanime.com/embed/kimetsu-1")
    'https://gogoanime.com/playlist/kimetsu-1.m3u8'
    """
    return episode_url.replace("/embed/", "/playlist/") + ".m3u8"


def is_valid_embed_url(url: str) -> bool:
    """
    Check whether a URL is a valid episode embed URL.

    >>> is_valid_embed_url("https://gogoanime.com/embed/kimetsu-1")
    True
    >>> is_valid_embed_url("https://gogoanime.com/watch/kimetsu-1")
    False
    >>> is_valid_embed_url("")
    False
    """
    return bool(url) and "/embed/" in url


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    keyword = "demon_slayer"
    embed_url = "https://gogoanime.com/embed/kimetsu-no-yaiba-1"

    print("URL building:")
    for name, fn in [
        ("f-string", build_search_url_fstring),
        ("urljoin", build_search_url_urljoin),
    ]:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(BASE_URL, keyword)
        elapsed = time.perf_counter() - t0
        print(f"  {name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")

    print("URL transform:")
    t0 = time.perf_counter()
    for _ in range(runs):
        transform_embed_to_playlist(embed_url)
    elapsed = time.perf_counter() - t0
    print(f"  {'replace+add':12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
