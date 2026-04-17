"""
HackerNews Top Posts – three markdown-formatting approaches + benchmark.

Approach 1: str.join with format (original)
Approach 2: list comprehension + join
Approach 3: io.StringIO buffer
"""

import io
import time

SAMPLE_STORIES = [
    {"title": "Python 4.0 released", "url": "https://python.org/news"},
    {"title": "New AI breakthrough", "url": "https://example.com/ai"},
    {"title": "Open source wins", "url": "https://example.com/oss"},
]


# ---------------------------------------------------------------------------
# Approach 1 – join with format (original)
# ---------------------------------------------------------------------------
def stories_to_markdown_join(stories: list[dict]) -> str:
    """
    Format stories as markdown using str.join and format.

    >>> print(stories_to_markdown_join([{"title": "T", "url": "https://u.com"}]))
    * [T](https://u.com)
    """
    return "\n".join("* [{title}]({url})".format(**s) for s in stories)


# ---------------------------------------------------------------------------
# Approach 2 – list comprehension
# ---------------------------------------------------------------------------
def stories_to_markdown_list(stories: list[dict]) -> str:
    """
    Format stories as markdown using a list comprehension.

    >>> print(stories_to_markdown_list([{"title": "T", "url": "https://u.com"}]))
    * [T](https://u.com)
    """
    lines = [f"* [{s['title']}]({s['url']})" for s in stories]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Approach 3 – StringIO buffer
# ---------------------------------------------------------------------------
def stories_to_markdown_stringio(stories: list[dict]) -> str:
    """
    Format stories as markdown using an io.StringIO buffer.

    >>> print(stories_to_markdown_stringio([{"title": "T", "url": "https://u.com"}]))
    * [T](https://u.com)
    """
    buf = io.StringIO()
    for i, s in enumerate(stories):
        if i:
            buf.write("\n")
        buf.write(f"* [{s['title']}]({s['url']})")
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 200_000) -> None:
    approaches = [
        ("join+format", stories_to_markdown_join),
        ("list comp", stories_to_markdown_list),
        ("StringIO", stories_to_markdown_stringio),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_STORIES)
        elapsed = time.perf_counter() - t0
        print(f"{name:15s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
