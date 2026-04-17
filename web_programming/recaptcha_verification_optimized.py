"""
reCAPTCHA Verification – three response-parsing approaches + benchmark.

Approach 1: .get() on JSON (original)
Approach 2: boolean cast on dict value
Approach 3: dataclass-based response model
"""

import time
from dataclasses import dataclass

SAMPLE_SUCCESS_RESPONSE = {"success": True, "challenge_ts": "2024-01-01T00:00:00Z", "hostname": "example.com"}
SAMPLE_FAIL_RESPONSE = {"success": False, "error-codes": ["invalid-input-response"]}


# ---------------------------------------------------------------------------
# Approach 1 – .get() (original)
# ---------------------------------------------------------------------------
def is_verified_get(response_json: dict) -> bool:
    """
    Check reCAPTCHA success using .get() with False default.

    >>> is_verified_get({"success": True})
    True
    >>> is_verified_get({"success": False})
    False
    >>> is_verified_get({})
    False
    """
    return response_json.get("success", False)


# ---------------------------------------------------------------------------
# Approach 2 – direct bool cast with key access
# ---------------------------------------------------------------------------
def is_verified_bool(response_json: dict) -> bool:
    """
    Check reCAPTCHA success using bool() on the 'success' key.

    >>> is_verified_bool({"success": True})
    True
    >>> is_verified_bool({"success": False})
    False
    >>> is_verified_bool({})
    False
    """
    return bool(response_json.get("success"))


# ---------------------------------------------------------------------------
# Approach 3 – dataclass model
# ---------------------------------------------------------------------------
@dataclass
class RecaptchaResponse:
    success: bool
    challenge_ts: str = ""
    hostname: str = ""
    error_codes: list | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "RecaptchaResponse":
        return cls(
            success=data.get("success", False),
            challenge_ts=data.get("challenge_ts", ""),
            hostname=data.get("hostname", ""),
            error_codes=data.get("error-codes"),
        )


def is_verified_dataclass(response_json: dict) -> bool:
    """
    Check reCAPTCHA success by parsing into a RecaptchaResponse dataclass.

    >>> is_verified_dataclass({"success": True, "hostname": "example.com"})
    True
    >>> is_verified_dataclass({"success": False})
    False
    """
    return RecaptchaResponse.from_dict(response_json).success


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 500_000) -> None:
    approaches = [
        (".get() default", is_verified_get),
        ("bool+get", is_verified_bool),
        ("dataclass", is_verified_dataclass),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_SUCCESS_RESPONSE)
        elapsed = time.perf_counter() - t0
        print(f"{name:18s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
