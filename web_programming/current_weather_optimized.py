"""
Current Weather – three response-parsing approaches + benchmark.

Approach 1: dict key access (standard)
Approach 2: .get() with nested fallback
Approach 3: dataclass model
"""

import time
from dataclasses import dataclass

SAMPLE_OWM_RESPONSE = {
    "name": "London",
    "main": {"temp": 285.5, "humidity": 80},
    "weather": [{"description": "light rain"}],
    "wind": {"speed": 5.2},
}


# ---------------------------------------------------------------------------
# Approach 1 – dict key access
# ---------------------------------------------------------------------------
def parse_weather_key(data: dict) -> dict:
    """
    Parse OpenWeatherMap response using direct key access.

    >>> r = parse_weather_key(SAMPLE_OWM_RESPONSE)
    >>> r["city"]
    'London'
    >>> r["temp_k"]
    285.5
    """
    return {
        "city": data["name"],
        "temp_k": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"],
    }


# ---------------------------------------------------------------------------
# Approach 2 – .get() with fallback
# ---------------------------------------------------------------------------
def parse_weather_get(data: dict, default: str = "N/A") -> dict:
    """
    Parse OpenWeatherMap response using .get() with defaults.

    >>> r = parse_weather_get(SAMPLE_OWM_RESPONSE)
    >>> r["city"]
    'London'
    >>> parse_weather_get({})["city"]
    'N/A'
    """
    main = data.get("main", {})
    weather = data.get("weather", [{}])
    wind = data.get("wind", {})
    return {
        "city": data.get("name", default),
        "temp_k": main.get("temp", default),
        "humidity": main.get("humidity", default),
        "description": weather[0].get("description", default) if weather else default,
        "wind_speed": wind.get("speed", default),
    }


# ---------------------------------------------------------------------------
# Approach 3 – dataclass
# ---------------------------------------------------------------------------
@dataclass
class WeatherSummary:
    city: str
    temp_k: float
    humidity: int
    description: str
    wind_speed: float


def parse_weather_dataclass(data: dict) -> WeatherSummary:
    """
    Parse OpenWeatherMap response into a typed WeatherSummary dataclass.

    >>> ws = parse_weather_dataclass(SAMPLE_OWM_RESPONSE)
    >>> ws.city
    'London'
    >>> ws.humidity
    80
    """
    return WeatherSummary(
        city=data["name"],
        temp_k=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        description=data["weather"][0]["description"],
        wind_speed=data["wind"]["speed"],
    )


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 300_000) -> None:
    approaches = [
        ("key access", parse_weather_key),
        ("get fallback", parse_weather_get),
        ("dataclass", parse_weather_dataclass),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_OWM_RESPONSE)
        elapsed = time.perf_counter() - t0
        print(f"{name:15s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.3f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
