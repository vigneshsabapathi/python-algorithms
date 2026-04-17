"""
Slack Message – three payload-building approaches + benchmark.

Approach 1: plain dict (original)
Approach 2: json.dumps string body
Approach 3: dataclass payload model
"""

import json
import time
from dataclasses import asdict, dataclass


# ---------------------------------------------------------------------------
# Approach 1 – plain dict (original)
# ---------------------------------------------------------------------------
def build_payload_dict(message: str) -> dict:
    """
    Build a Slack webhook payload as a plain dict.

    >>> build_payload_dict("Hello!")
    {'text': 'Hello!'}
    """
    return {"text": message}


# ---------------------------------------------------------------------------
# Approach 2 – pre-serialized JSON string
# ---------------------------------------------------------------------------
def build_payload_json(message: str) -> str:
    """
    Build a Slack webhook payload as a pre-serialized JSON string.

    >>> import json
    >>> json.loads(build_payload_json("Hello!"))
    {'text': 'Hello!'}
    """
    return json.dumps({"text": message})


# ---------------------------------------------------------------------------
# Approach 3 – dataclass
# ---------------------------------------------------------------------------
@dataclass
class SlackPayload:
    text: str

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(asdict(self))


def build_payload_dataclass(message: str) -> dict:
    """
    Build a Slack webhook payload via a SlackPayload dataclass.

    >>> build_payload_dataclass("Hello!")
    {'text': 'Hello!'}
    """
    return SlackPayload(text=message).to_dict()


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    message = "Build succeeded for commit abc1234!"
    approaches = [
        ("plain dict", build_payload_dict),
        ("json.dumps", build_payload_json),
        ("dataclass", build_payload_dataclass),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(message)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
