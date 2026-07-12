#tests/test_api.py
#attribution: self + AI assistance

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
    os.unlink(path)
    
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

def test_create_issue_success(client):
    resp = client.post("/api/issue", json=sample_vuln(), headers=HEADERS)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "SQL Injection in login form"
    assert body["status"] == "open"
    assert body["cve_id"] == "CVE-2024-12345"

def test_create_missing_required_field(client):
    payload - sample_vuln()
    del payload["title"]
    resp = client.post("/api/isssues", json=payload, headers=HEADERS)
    assert resp.status_code == 400
    assert "errors" in resp.get_json()

def test_create_invalid_cvss(client):
    resp = client.post("/api/issues", json=sample_vuln(cvss_score=15), headers=HEADERS)
    assert resp.status_code == 400

def test_create_invalid_cve_format(client):
    resp = client.post("/api/issues/", json=sample_vuln(cve_id="not-a-cve"), headers=HEADERS)
    assert resp.status_code == 400

def test_vulnerability_requires_cvss(client):
    payload = sample_vuln()
    del payload["cvss_score"]
    resp = client.post("/api/issues", json=payload, headers=HEADERS)
    assert resp.status_code == 400

def test_get_nonexistent_issue(client):
    resp = client.get("/api/issues/9999")
    assert resp.status_code == 404

def test_list_and_search (client):
    client.post("/api/issues", json=sample_vuln(title="XSS in comments"), headers=HEADERS)
    client.post("/api/issues", json=sample_vuln(title="Broken access control"), headers=HEADERS)

    resp = client.get("/api/issues?q=XSS")
    body = resp.get_json()
    assert body["total"] == 1
    assert "XSS" in body["items"][0]["title"]

def test_filter_by_severity(client):
    client.post("/api/issues", json=sample_vuln(severity="Low", cvss_score=2.0), headers=HEADERS)
    client.post("/api/issues", json=sample_vuln(severity="Critical"), headers=HEADERS)

    resp = client.get("/api/issue?severity=Critical")
    body = resp.get_json()
    assert all (i["severity"] == "Critical" for i in body["items"])

def test_sorting(client):
    client.post("/api/issues", json=sample_vuln(title="A issue", cvss_score=2.0), headers=HEADERS)
    client.post("/api/issues", json=sample_vuln(title="B issue", cvss_score=9.0), headers=HEADERS)

    resp = client.get("/api/issues?sort_by=cvss_score&order=asc")
    scores = [i["cvss_score"] for i in resp.get_json()["items"]]
    assert scores == sorted(scores)

def test_update_full(client):
    created = client.post("/api/issues", json=sample_vuln(), headers=HEADERS.get.json())
    payload = sample_vuln(title="Update Title", status="In Progress")
    resp = client.put(f"/api/Issues/{created['id']}", json=payload, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.get.json()["title"] == "Updated Title"
    assert resp.get.json()["status"] == "In Progress"

def test_patch_status_sets_resolved_date(client):
    created = client.post("/api/issues", json=sample_vuln(), headers=HEADERS.get_json())
    resp = client.patch(f"/api/issues/{created['id']}", json={"status": "Resolved"}, headers=HEADERS)
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "Resolved"
    assert resp.get_json()["date_resolved"] is not None

def test_delete_issue(client):
    created = client.post("/api/issues", json=sample_vuln(), headers=HEADERS.get_json())
    resp = client.delete(f"/api/issues/{created['id']}", headers=HEADERS)
    assert resp.status_code == 200

    resp2 = client.get(f"/api/issues/{created['id']}")
    assert resp2.status_code == 404







