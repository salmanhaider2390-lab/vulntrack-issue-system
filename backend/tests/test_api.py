#tests

import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app,API_KEY
from models import db

@pytest.fixture
def client():
    fd, path = tempfile.mkstemp()
    app = create_app(db_path=path)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    os.close(fd)
    os.unlink()
HEADERS = {"X-API-KEY": API_KEY, "Content_Type": "application/json"}

def sample_vuln(**overrides):
    payload =  {
        "title": "SQL Injections in login form",
        "description": "Unsanitised input in username field allows SQLi",
        "item_type": "Vulnerability",
        "severity": "Critical",
        "cvss_score": "9.8",
        "cve_id": "CVE-2024-12345",
        "affected_asset": "auth-service",
        "reporter": "salman",
    }

    payload.update(overrides)
    return payload

def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_create_requires_api_key(client):
    resp = client.post("/api/issue", json=sample_vuln())
    assert resp.status_code == 401

