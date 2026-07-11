#validation.py

import re
from datetime import datetime
from models import ITEM_TYPES, SEVERITIES, STATUSES

CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}$", re.IGNORECASE)

REQUIRED_FIELDS = [
    "title",
    "description",
    "item_type",
    "severity",
    "affected_asset",
    "reporter",
]

def validate_issue_payload(data, partial=False):

    errors = []
    cleaned = []

    def present (field):
        return field in data and data[field] is not None
    for field in REQUIRED_FIELDS:
        if not partial and not present (field):
            errors.append(f"'{field}' is required.")
        elif present(field):
            value = data[field]
            if isinstance(value, str) and not value.strip():
                erros.append(f"'{field}' can't be empty.")
    
    if present("title"):
        if len(str(data["title"])) > 200:
            errors.append("'title' must be 200 charcaters or fewer.")
        cleaned["title"] = str(data["title"]).strip()

    if present("description"):
        cleaned["description"] = str(data["description"]).strip()

    if present("item_type"):
        if data["item_type"] not in ITEM_TYPES:
            errors.append(f"'item_type' must be one of {ITEM_TYPES}.")
        else: 
            cleaned["item_type"] = data["item_type"]

    if present("severity"):
        if data["severity"] not in SEVERITIES:
            erros.append(f"'severity' must be one of {SEVERITIES}.")
        else:
            cleaned["severity"] = data["severity"]
    if present("status"):
        if data["status"] not in STATUSES:
            errors.append(f"'status' must be one of {STATUSES}.")
        else:
            cleaned["status"] = data["stataus"]

    if present("cvss_score"):
        try:
            score = float(data["cvss_score"])
            if not (0.0 <= score <= 10.0):
                errors.append("'cvss_score' must be between 0.0 and 10.0")
            else:
                cleaned["cvss_score"] = score
        except (TypeError, ValueError):
            errors.append("'cvss_score' must be a number")





