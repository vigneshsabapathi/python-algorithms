"""
Fetch BBC News – three response-formatting approaches + benchmark.

Approach 1: enumerate loop (original)
Approach 2: list comprehension
Approach 3: map + enumerate
"""

import time

SAMPLE_ARTICLES = [
    {"title": "UK inflation rises to 4%", "author": "BBC News"},
    {"title": "AI regulation debated in parliament", "author": "BBC News"},
    {"title": "New species discovered in Amazon", "author": "BBC Environment"},
]


# ---------------------------------------------------------------------------
# Approach 1 – enumerate loop (original)
# ---------------------------------------------------------------------------
def format_articles_loop(articles: list[dict]) -> list[str]:
    """
    Format articles using an enumerate loop.

    >>> format_articles_loop([{"title": "A"}, {"title": "B"}])
    ['1.) A', '2.) B']
    """
    result = []
    for i, article in enumerate(articles, 1):
        result.append(f"{i}.) {article['title']}")
    return result


# ---------------------------------------------------------------------------
# Approach 2 – list comprehension
# ---------------------------------------------------------------------------
def format_articles_listcomp(articles: list[dict]) -> list[str]:
    """
    Format articles using a list comprehension.

    >>> format_articles_listcomp([{"title": "A"}, {"title": "B"}])
    ['1.) A', '2.) B']
    """
    return [f"{i}.) {a['title']}" for i, a in enumerate(articles, 1)]


# ---------------------------------------------------------------------------
# Approach 3 – map
# ---------------------------------------------------------------------------
def format_articles_map(articles: list[dict]) -> list[str]:
    """
    Format articles using map + lambda.

    >>> format_articles_map([{"title": "A"}, {"title": "B"}])
    ['1.) A', '2.) B']
    """
    return list(
        map(lambda ia: f"{ia[0]}.) {ia[1]['title']}", enumerate(articles, 1))
    )


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 300_000) -> None:
    approaches = [
        ("loop", format_articles_loop),
        ("list comp", format_articles_listcomp),
        ("map", format_articles_map),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_ARTICLES)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
