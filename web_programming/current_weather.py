"""
Fetch current weather data from OpenWeatherMap and/or Weatherstack APIs.

Set OPENWEATHERMAP_API_KEY and/or WEATHERSTACK_API_KEY environment variables.
"""

import os

import requests

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY", "")

OPENWEATHERMAP_URL_BASE = "https://api.openweathermap.org/data/2.5/weather"
WEATHERSTACK_URL_BASE = "http://api.weatherstack.com/current"


def current_weather(location: str) -> list[dict]:
    """
    Return weather data for a location from configured API providers.

    Raises ValueError if no API keys are set.

    >>> current_weather("location")
    Traceback (most recent call last):
        ...
    ValueError: No API keys provided or no valid data returned.
    """
    weather_data = []
    if OPENWEATHERMAP_API_KEY:
        params = {"q": location, "appid": OPENWEATHERMAP_API_KEY}
        resp = requests.get(OPENWEATHERMAP_URL_BASE, params=params, timeout=10)
        weather_data.append({"OpenWeatherMap": resp.json()})
    if WEATHERSTACK_API_KEY:
        params = {"query": location, "access_key": WEATHERSTACK_API_KEY}
        resp = requests.get(WEATHERSTACK_URL_BASE, params=params, timeout=10)
        weather_data.append({"Weatherstack": resp.json()})
    if not weather_data:
        raise ValueError("No API keys provided or no valid data returned.")
    return weather_data


if __name__ == "__main__":
    from pprint import pprint

    location = input("Enter a location (city name or latitude,longitude): ").strip()
    if location:
        try:
            for forecast in current_weather(location):
                pprint(forecast)
        except ValueError as e:
            print(repr(e))
