"""IPv4 validation — variants + benchmark."""

import re
import time
import ipaddress


def ipv4_manual(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p or not p.isdigit():
            return False
        if len(p) > 1 and p[0] == "0":
            return False
        if int(p) > 255:
            return False
    return True


_IPV4_RE = re.compile(
    r"^((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"
)


def ipv4_regex(ip):
    return bool(_IPV4_RE.match(ip))


def ipv4_stdlib(ip):
    try:
        ipaddress.IPv4Address(ip)
        # IPv4Address accepts leading zeros in older Python; strict check needed
        return ip == str(ipaddress.IPv4Address(ip))
    except (ValueError, ipaddress.AddressValueError):
        return False


def benchmark():
    tests = ["192.168.0.1", "256.1.1.1", "1.2.3", "01.2.3.4", "0.0.0.0", "255.255.255.255"] * 10_000
    for name, fn in [
        ("manual_split", ipv4_manual),
        ("regex", ipv4_regex),
        ("ipaddress_stdlib", ipv4_stdlib),
    ]:
        start = time.perf_counter()
        hits = sum(1 for t in tests if fn(t))
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} valid={hits}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
