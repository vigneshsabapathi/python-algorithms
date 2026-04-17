"""
Scrape prescription drug prices from WellRx.com.

Given a drug name and zip code, returns a list of pharmacy name/price dicts.
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.wellrx.com/prescriptions/{}/{}/?freshSearch=true"


def build_wellrx_url(drug_name: str, zip_code: str) -> str:
    """
    Build the WellRx search URL for a drug and zip code.

    >>> build_wellrx_url("eliquis", "30303")
    'https://www.wellrx.com/prescriptions/eliquis/30303/?freshSearch=true'
    >>> build_wellrx_url("lipitor", "10001")
    'https://www.wellrx.com/prescriptions/lipitor/10001/?freshSearch=true'
    """
    return BASE_URL.format(drug_name, zip_code)


def fetch_pharmacy_and_price_list(drug_name: str, zip_code: str) -> list | None:
    """
    Return a list of {'pharmacy_name': ..., 'price': ...} dicts, or None on failure.

    >>> fetch_pharmacy_and_price_list(None, None)

    >>> fetch_pharmacy_and_price_list("eliquis", "30303")  # doctest: +SKIP
    [{'pharmacy_name': 'CVS Pharmacy', 'price': '$12.00'}, ...]
    """
    try:
        if not drug_name or not zip_code:
            return None
        request_url = build_wellrx_url(drug_name, zip_code)
        response = requests.get(request_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        pharmacy_price_list = []
        grid_list = soup.find_all("div", {"class": "grid-x pharmCard"})
        for grid in grid_list:
            pharmacy_name = grid.find("p", {"class": "list-title"}).text
            price = grid.find("span", {"class": "price price-large"}).text
            pharmacy_price_list.append(
                {"pharmacy_name": pharmacy_name, "price": price}
            )
        return pharmacy_price_list
    except (requests.HTTPError, ValueError):
        return None


if __name__ == "__main__":
    drug_name = input("Enter drug name: ").strip()
    zip_code = input("Enter zip code: ").strip()
    results = fetch_pharmacy_and_price_list(drug_name, zip_code)
    if results:
        print(f"\nSearch results for {drug_name} at location {zip_code}:")
        for item in results:
            print(f"Pharmacy: {item['pharmacy_name']}  Price: {item['price']}")
    else:
        print(f"No results found for {drug_name}.")
