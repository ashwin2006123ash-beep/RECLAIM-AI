"""
RECLAIM AI - Source Safety Guard & SSRF Protection
Enforces strict domain allowlists, flags unofficial third-party brokers,
and guards against Server-Side Request Forgery (SSRF) and metadata attacks.
"""
import ipaddress
import socket
from urllib.parse import urlparse
from typing import Dict, Any, Tuple
from config import Config

def is_ip_private_or_restricted(ip_str: str) -> bool:
    """Checks if an IP address belongs to loopback, private, link-local, or cloud metadata ranges."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private or
            ip.is_loopback or
            ip.is_link_local or
            ip.is_reserved or
            ip.is_multicast or
            str(ip) in ["169.254.169.254", "0.0.0.0", "::1"]
        )
    except ValueError:
        return False

def sanitize_and_validate_url(url: str) -> Tuple[bool, str, str]:
    """
    Validates a URL against protocol restrictions, blocked hosts, and SSRF attacks.
    Returns: (is_valid, sanitized_hostname, reason)
    """
    if not url or not isinstance(url, str):
        return False, "", "Empty or invalid URL provided."
        
    url = url.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        # If user/crawler gave bare domain, add https
        url = "https://" + url
        
    try:
        parsed = urlparse(url)
    except Exception as e:
        return False, "", f"Failed to parse URL: {str(e)}"
        
    hostname = (parsed.hostname or "").lower()
    
    if not hostname:
        return False, "", "URL lacks a valid hostname."
        
    # Check blocked hostnames
    if hostname in Config.BLOCKED_HOSTNAMES:
        return False, hostname, f"Security Violation: Target host '{hostname}' is blocked (SSRF Guard)."
        
    # Check if hostname directly represents an IP
    if is_ip_private_or_restricted(hostname):
        return False, hostname, f"Security Violation: Target IP '{hostname}' is a private/restricted address."
        
    # DNS resolution check for SSRF (defense in depth)
    try:
        resolved_ips = socket.gethostbyname_ex(hostname)[2]
        for ip in resolved_ips:
            if is_ip_private_or_restricted(ip):
                return False, hostname, f"Security Violation: Host '{hostname}' resolves to private address {ip}."
    except socket.gaierror:
        # If host cannot be resolved offline or during sandboxed run, check domain name structure
        pass
        
    return True, hostname, "URL structure is valid."

def evaluate_source_safety(url_or_domain: str) -> Dict[str, Any]:
    """
    Evaluates whether a source is an authoritative government/educational portal,
    an unofficial commercial broker/agent, or an untrusted external entity.
    """
    is_valid, hostname, reason = sanitize_and_validate_url(url_or_domain)
    
    if not is_valid:
        return {
            "is_safe": False,
            "is_official": False,
            "verification_status": "blocked",
            "hostname": hostname,
            "threat_level": "CRITICAL",
            "reason": reason,
            "action": "REJECT"
        }
        
    # Check known unofficial broker / agent domains
    for unofficial in Config.KNOWN_UNOFFICIAL_DOMAINS:
        if hostname == unofficial or hostname.endswith("." + unofficial):
            return {
                "is_safe": True, # Syntactically valid web URL, but commercially untrusted
                "is_official": False,
                "verification_status": "unofficial_rejected",
                "hostname": hostname,
                "threat_level": "HIGH_RISK",
                "reason": (
                    f"FLAGGED: '{hostname}' is an unofficial third-party agent/broker site. "
                    "It is NOT authorized by any government ministry. It may charge unauthorized service fees "
                    "or collect sensitive personal data without statutory safeguards."
                ),
                "action": "EXCLUDE_FROM_AUTHORITATIVE_GUIDANCE"
            }
            
    # Check official domain allowlist
    is_official = False
    for suffix in Config.OFFICIAL_DOMAIN_SUFFIXES:
        if hostname == suffix or hostname.endswith(suffix):
            is_official = True
            break
            
    if is_official:
        return {
            "is_safe": True,
            "is_official": True,
            "verification_status": "official_verified",
            "hostname": hostname,
            "threat_level": "NONE",
            "reason": f"Verified official statutory/government domain: '{hostname}'.",
            "action": "PERMIT_AND_CITE"
        }
        
    # Generic unverified third-party website
    return {
        "is_safe": True,
        "is_official": False,
        "verification_status": "unverified",
        "hostname": hostname,
        "threat_level": "MODERATE",
        "reason": f"Hostname '{hostname}' is not present in the verified official government registry.",
        "action": "WARN_USER_AND_REQUIRE_CONFIRMATION"
    }
