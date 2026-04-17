"""
Reddit – three approaches to filtering subreddit post data + benchmark.

Approach 1: dict comprehension (original)
Approach 2: operator.itemgetter for field extraction
Approach 3: dataclass-based typed post model
"""

import time
from dataclasses import dataclass
from operator import itemgetter
from typing import Any


SAMPLE_CHILDREN = [
    {
        "data": {
            "title": "Learn Python in 30 days",
            "url": "https://example.com/python",
            "selftext": "Here is how...",
            "score": 1500,
            "ups": 1600,
        }
    },
    {
        "data": {
            "title": "Best Python resources",
            "url": "https://example.com/resources",
            "selftext": "Check these out...",
            "score": 900,
            "ups": 950,
        }
    },
]


# ---------------------------------------------------------------------------
# Approach 1 – dict comprehension (original style)
# ---------------------------------------------------------------------------
def extract_fields_dict(children: list[dict], fields: list[str]) -> dict[int, dict]:
    """
    Extract selected fields from Reddit children using dict comprehension.

    >>> result = extract_fields_dict(SAMPLE_CHILDREN, ["title", "score"])
    >>> result[0]["title"]
    'Learn Python in 30 days'
    >>> result[1]["score"]
    900
    """
    return {
        idx: {field: children[idx]["data"][field] for field in fields}
        for idx in range(len(children))
    }


# ---------------------------------------------------------------------------
# Approach 2 – itemgetter
# ---------------------------------------------------------------------------
def extract_fields_itemgetter(children: list[dict], fields: list[str]) -> dict[int, dict]:
    """
    Extract selected fields using operator.itemgetter for repeated field access.

    >>> result = extract_fields_itemgetter(SAMPLE_CHILDREN, ["title", "score"])
    >>> result[0]["title"]
    'Learn Python in 30 days'
    >>> result[1]["score"]
    900
    """
    getter = itemgetter(*fields)
    result = {}
    for idx, child in enumerate(children):
        values = getter(child["data"])
        if len(fields) == 1:
            result[idx] = {fields[0]: values}
        else:
            result[idx] = dict(zip(fields, values))
    return result


# ---------------------------------------------------------------------------
# Approach 3 – dataclass model
# ---------------------------------------------------------------------------
@dataclass
class RedditPost:
    title: str
    url: str
    selftext: str
    score: int


def extract_as_dataclass(children: list[dict]) -> list[RedditPost]:
    """
    Parse Reddit children into typed RedditPost dataclass instances.

    >>> posts = extract_as_dataclass(SAMPLE_CHILDREN)
    >>> posts[0].title
    'Learn Python in 30 days'
    >>> posts[1].score
    900
    """
    return [
        RedditPost(
            title=c["data"]["title"],
            url=c["data"]["url"],
            selftext=c["data"]["selftext"],
            score=c["data"]["score"],
        )
        for c in children
    ]


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 100_000) -> None:
    fields = ["title", "score"]
    print("Dict comprehension vs itemgetter vs dataclass:")
    for name, fn, kwargs in [
        ("dict comp", extract_fields_dict, {"fields": fields}),
        ("itemgetter", extract_fields_itemgetter, {"fields": fields}),
    ]:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_CHILDREN, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f"  {name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")

    t0 = time.perf_counter()
    for _ in range(runs):
        extract_as_dataclass(SAMPLE_CHILDREN)
    elapsed = time.perf_counter() - t0
    print(f"  {'dataclass':12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
