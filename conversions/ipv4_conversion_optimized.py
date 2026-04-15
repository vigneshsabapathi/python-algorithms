"""
IPv4 Conversion - Optimized Variants with Benchmarks
"""

import timeit
import struct
import socket


def ipv4_to_int_manual(ip: str) -> int:
    """
    Manual bit-shifting.

    >>> ipv4_to_int_manual("192.168.1.1")
    3232235777
    """
    result = 0
    for octet in ip.split("."):
        result = (result << 8) | int(octet)
    return result


def ipv4_to_int_struct(ip: str) -> int:
    """
    Using struct.unpack for network byte order.

    >>> ipv4_to_int_struct("192.168.1.1")
    3232235777
    """
    return struct.unpack("!I", socket.inet_aton(ip))[0]


def ipv4_to_int_sum(ip: str) -> int:
    """
    Sum with enumerate powers.

    >>> ipv4_to_int_sum("192.168.1.1")
    3232235777
    """
    octets = ip.split(".")
    return sum(int(o) << (8 * (3 - i)) for i, o in enumerate(octets))


def benchmark():
    test_input = "192.168.1.1"
    number = 100_000
    print(f"Benchmark: converting '{test_input}' ({number:,} iterations)\n")
    results = []
    for label, func in [("Manual shift", ipv4_to_int_manual),
                         ("Struct/socket", ipv4_to_int_struct),
                         ("Sum/enumerate", ipv4_to_int_sum)]:
        t = timeit.timeit(lambda: func(test_input), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
