"""
Get geolocation data for an IP address using the ipinfo.io API.

Returns city, region, and country for the given IP.
"""

import requests

IPINFO_URL = "https://ipinfo.io/{ip}/json"


def build_ipinfo_url(ip_address: str) -> str:
    """
    Build the ipinfo.io API URL for a given IP address.

    >>> build_ipinfo_url("8.8.8.8")
    'https://ipinfo.io/8.8.8.8/json'
    >>> build_ipinfo_url("1.1.1.1")
    'https://ipinfo.io/1.1.1.1/json'
    """
    return IPINFO_URL.format(ip=ip_address)


def get_ip_geolocation(ip_address: str) -> str:
    """
    Return a formatted location string for the given IP address.

    >>> get_ip_geolocation("8.8.8.8")  # doctest: +SKIP
    'Location: Mountain View, California, US'
    >>> get_ip_geolocation("invalid_ip")  # doctest: +SKIP
    'Location data not found.'
    """
    try:
        url = build_ipinfo_url(ip_address)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "city" in data and "region" in data and "country" in data:
            return f"Location: {data['city']}, {data['region']}, {data['country']}"
        return "Location data not found."
    except requests.RequestError as e:
        return f"Request error: {e}"
    except ValueError as e:
        return f"JSON parsing error: {e}"


if __name__ == "__main__":
    ip_address = input("Enter an IP address: ").strip()
    print(get_ip_geolocation(ip_address))
