"""
Nexus Security and SSRF Prevention Module
Enforces tenant isolation, secure secret hashing, and outbound URL validation.
"""

import hashlib
import ipaddress
import re
import socket
import urllib.parse
from typing import Tuple


def hash_secret(raw_secret: str) -> str:
    """Hash an API secret with SHA-256 for secure storage."""
    return hashlib.sha256(raw_secret.encode("utf-8")).hexdigest()


def generate_agent_key() -> Tuple[str, str, str]:
    """
    Generate an agent key pair.
    Returns: (full_token, prefix, hashed_secret)
    """
    import secrets
    prefix = f"nx_agt_{secrets.token_hex(4)}"
    secret = secrets.token_urlsafe(32)
    full_token = f"{prefix}.{secret}"
    hashed = hash_secret(full_token)
    return full_token, prefix, hashed


def generate_owner_key() -> Tuple[str, str, str]:
    """
    Generate an owner API key pair.
    Returns: (full_token, prefix, hashed_secret)
    """
    import secrets
    prefix = f"nx_own_{secrets.token_hex(4)}"
    secret = secrets.token_urlsafe(32)
    full_token = f"{prefix}.{secret}"
    hashed = hash_secret(full_token)
    return full_token, prefix, hashed


# Cloud metadata and private IP CIDRs blocked from SSRF
FORBIDDEN_NETWORKS = [
    ipaddress.ip_network("127.0.0.0/8"),      # Loopback
    ipaddress.ip_network("10.0.0.0/8"),       # Private Class A
    ipaddress.ip_network("172.16.0.0/12"),    # Private Class B
    ipaddress.ip_network("192.168.0.0/16"),   # Private Class C
    ipaddress.ip_network("169.254.0.0/16"),   # Link-Local & Cloud Metadata (169.254.169.254)
    ipaddress.ip_network("::1/128"),          # IPv6 Loopback
    ipaddress.ip_network("fc00::/7"),         # IPv6 Unique Local
    ipaddress.ip_network("fe80::/10"),        # IPv6 Link-Local
]


def validate_seller_endpoint_url(url: str, allow_localhost_for_tests: bool = False) -> Tuple[bool, str]:
    """
    Validates that a seller endpoint URL does not target loopback, private networks,
    or cloud instance metadata (preventing SSRF attacks per OWASP guidelines).
    """
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception as e:
        return False, f"Malformed URL: {e}"

    if parsed.scheme not in ("https", "mock", "http"):
        return False, f"Unsupported scheme '{parsed.scheme}'. Only HTTPS is permitted in production."

    if not allow_localhost_for_tests and parsed.scheme != "https":
        return False, "Only HTTPS seller endpoints are permitted in production."

    hostname = parsed.hostname
    if not hostname:
        return False, "URL missing hostname."

    if allow_localhost_for_tests and hostname in ("localhost", "127.0.0.1", "testserver"):
        return True, "Valid test endpoint"

    # Explicitly block known cloud metadata hostnames
    if hostname.lower() in ("metadata.google.internal", "metadata", "instance-data"):
        return False, "Targeting cloud metadata services is strictly forbidden."

    # Resolve IP and check against forbidden networks
    try:
        ip_addresses = socket.getaddrinfo(hostname, None)
        for family, _, _, _, sockaddr in ip_addresses:
            ip_str = sockaddr[0]
            ip_obj = ipaddress.ip_address(ip_str)
            for forbidden_net in FORBIDDEN_NETWORKS:
                if ip_obj in forbidden_net:
                    return False, f"Endpoint resolves to forbidden network address {ip_str}."
    except socket.gaierror:
        if not allow_localhost_for_tests:
            return False, f"DNS resolution failed for hostname '{hostname}'. Unresolvable endpoints are rejected."
        pass

    return True, "Valid seller endpoint"

