"""
Instagram Crawler – three JSON-extraction approaches + benchmark.

Approach 1: json.loads with string slicing (original)
Approach 2: json.loads + nested key traversal
Approach 3: regex-based JSON fragment extraction
"""

import json
import re
import time

# Minimal synthetic JSON that mimics Instagram's embedded script data
_MOCK_DATA = {
    "config": {},
    "entry_data": {
        "ProfilePage": [
            {
                "graphql": {
                    "user": {
                        "username": "github",
                        "full_name": "GitHub",
                        "biography": "Built for developers.",
                        "is_verified": True,
                        "is_private": False,
                        "edge_followed_by": {"count": 200000},
                        "edge_follow": {"count": 500},
                        "edge_owner_to_timeline_media": {"count": 300},
                        "profile_pic_url_hd": "https://instagram.com/pic.jpg",
                        "business_email": "support@github.com",
                        "external_url": "https://github.com/readme",
                    }
                }
            }
        ]
    },
}
MOCK_SCRIPT_CONTENT = json.dumps(_MOCK_DATA)


# ---------------------------------------------------------------------------
# Approach 1 – slice + json.loads (original approach)
# ---------------------------------------------------------------------------
def extract_user_slice(script_content: str) -> dict:
    """
    Extract user dict using string slicing from '{"config"' marker.

    >>> user = extract_user_slice(MOCK_SCRIPT_CONTENT)
    >>> user["username"]
    'github'
    """
    start = script_content.find('{"config"')
    data = json.loads(script_content[start:-1] if script_content.endswith(";") else script_content[start:])
    return data["entry_data"]["ProfilePage"][0]["graphql"]["user"]


# ---------------------------------------------------------------------------
# Approach 2 – full json.loads with key path
# ---------------------------------------------------------------------------
def extract_user_full_parse(script_content: str) -> dict:
    """
    Parse the entire JSON and navigate to user data.

    >>> user = extract_user_full_parse(MOCK_SCRIPT_CONTENT)
    >>> user["is_verified"]
    True
    """
    data = json.loads(script_content)
    return data["entry_data"]["ProfilePage"][0]["graphql"]["user"]


# ---------------------------------------------------------------------------
# Approach 3 – regex to isolate user JSON block
# ---------------------------------------------------------------------------
_USERNAME_RE = re.compile(r'"username"\s*:\s*"([^"]+)"')


def extract_username_regex(script_content: str) -> str:
    """
    Extract just the username from the script content via regex (fast for single field).

    >>> extract_username_regex(MOCK_SCRIPT_CONTENT)
    'github'
    >>> extract_username_regex('{"username": "testuser"}')
    'testuser'
    """
    m = _USERNAME_RE.search(script_content)
    return m.group(1) if m else ""


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 10_000) -> None:
    approaches_full = [
        ("slice+parse", extract_user_slice),
        ("full parse", extract_user_full_parse),
    ]
    for name, fn in approaches_full:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(MOCK_SCRIPT_CONTENT)
        elapsed = time.perf_counter() - t0
        print(f"{name:15s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")

    runs_re = 100_000
    t0 = time.perf_counter()
    for _ in range(runs_re):
        extract_username_regex(MOCK_SCRIPT_CONTENT)
    elapsed = time.perf_counter() - t0
    print(f"{'regex field':15s}: {runs_re} runs in {elapsed:.4f}s ({elapsed/runs_re*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
