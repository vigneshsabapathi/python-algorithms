"""
Extract email addresses found at a given URL by crawling all internal links.

Uses a custom HTMLParser to collect anchor hrefs, then regex-matches emails.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib import parse

import requests


class LinkParser(HTMLParser):
    """HTML parser that collects all href values from anchor tags."""

    def __init__(self, domain: str) -> None:
        super().__init__()
        self.urls: list[str] = []
        self.domain = domain

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value not in (*self.urls, "", "#"):
                    url = parse.urljoin(self.domain, value)
                    self.urls.append(url)


def get_domain_name(url: str) -> str:
    """
    Return the root domain (e.g., 'example.com') from a URL.

    >>> get_domain_name("https://a.b.c.d/e/f?g=h,i=j#k")
    'c.d'
    >>> get_domain_name("Not a URL!")
    ''
    """
    return ".".join(get_sub_domain_name(url).split(".")[-2:])


def get_sub_domain_name(url: str) -> str:
    """
    Return the full netloc (e.g., 'sub.example.com') from a URL.

    >>> get_sub_domain_name("https://a.b.c.d/e/f?g=h,i=j#k")
    'a.b.c.d'
    >>> get_sub_domain_name("Not a URL!")
    ''
    """
    return parse.urlparse(url).netloc


def emails_from_url(url: str = "https://github.com") -> list[str]:
    """
    Crawl a URL and all its internal links to find email addresses.

    >>> emails_from_url("https://github.com")  # doctest: +SKIP
    ['support@github.com']
    """
    domain = get_domain_name(url)
    parser = LinkParser(domain)
    try:
        r = requests.get(url, timeout=10)
        parser.feed(r.text)
        valid_emails: set[str] = set()
        for link in parser.urls:
            if not link.startswith(("http://", "https://")):
                link = parse.urljoin(f"https://{domain}", link)
            try:
                read = requests.get(link, timeout=10)
                for email in re.findall("[a-zA-Z0-9]+@" + domain, read.text):
                    valid_emails.add(email)
            except (ValueError, requests.RequestException):
                pass
    except (ValueError, requests.RequestException):
        raise SystemExit(1)
    return sorted(valid_emails)


if __name__ == "__main__":
    emails = emails_from_url("https://github.com")
    print(f"{len(emails)} emails found:")
    print("\n".join(sorted(emails)))
