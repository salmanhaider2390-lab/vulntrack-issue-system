# seed_data.py
# Attribution: self + Ai Assitance
# Populates the database with sample issues/vulnerabilities for demo purposes.
# Usage: python seed_data.py

import requests

BASE_URL = "http://127.0.0.1:5000/api/issues"
HEADERS = {"X-API-Key": "vuln-track-sa121417", "Content-Type": "application/json"}

SAMPLE_ISSUES = [
    {
        "title": "SQL Injection in customer login form",
        "description": "The login form does not sanitise the username parameter, allowing SQLi.",
        "item_type": "Vulnerability",
        "severity": "Critical",
        "cvss_score": 9.8,
        "cve_id": "CVE-2024-10001",
        "affected_asset": "auth-service (prod)",
        "reporter": "s.usman",
        "assignee": "app-sec-team",
    },
    {
        "title": "Outdated OpenSSL version on payment gateway",
        "description": "Payment gateway runs OpenSSL 1.0.2, vulnerable to several known CVEs.",
        "item_type": "Vulnerability",
        "severity": "High",
        "cvss_score": 7.5,
        "cve_id": "CVE-2023-50164",
        "affected_asset": "payment-gateway-01",
        "reporter": "s.usman",
        "assignee": "infra-team",
    },
    {
        "title": "Missing rate limiting on password reset endpoint",
        "description": "The /reset-password endpoint has no rate limiting, enabling brute force / enumeration.",
        "item_type": "Vulnerability",
        "severity": "Medium",
        "cvss_score": 5.3,
        "affected_asset": "api-gateway",
        "reporter": "soc-analyst-1",
    },
    {
        "title": "Dashboard chart renders incorrectly on Safari",
        "description": "The reporting dashboard chart overflows its container on Safari 17.",
        "item_type": "Bug",
        "severity": "Low",
        "affected_asset": "internal-dashboard",
        "reporter": "qa-team",
    },
    {
        "title": "Add MFA support for admin console",
        "description": "Request to add multi-factor authentication for all admin console logins.",
        "item_type": "Feature Request",
        "severity": "Informational",
        "affected_asset": "admin-console",
        "reporter": "ciso-office",
    },
]