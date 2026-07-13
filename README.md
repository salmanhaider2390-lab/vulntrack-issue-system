# Issue &amp; Vulnerability Tracking System — VulnTrack Company

A REST API-based issue and vulnerability tracker built for [module code / assignment name].
Backend: **Flask** + **Flask-SQLAlchemy** + **SQLite**. Frontend: a lightweight **vanilla HTML/JS** single-page client.

---

## 1. Requirements

### 1.1 Purpose
Track software issues, bugs, feature requests, and security vulnerabilities affecting
VulnTrack Company' systems, with enough structure to support triage,
remediation tracking, and management reporting.

### 1.2 Data requirements
Each tracked item has:

| Field | Type | Notes |
|---|---|---|
| id | int | PK, auto-increment |
| title | string(200) | required |
| description | text | required |
| item_type | enum | Bug / Vulnerability / Feature Request |
| severity | enum | Critical / High / Medium / Low / Informational |
| cvss_score | float 0.0–10.0 | required when `item_type=Vulnerability` |
| cve_id | string | optional, must match `CVE-YYYY-NNNN` if present |
| status | enum | Open / In Progress / Resolved / Closed / Won't Fix |
| affected_asset | string | required — system/service affected |
| company | string | defaults to VulnTrack Company |
| reporter | string | required |
| assignee | string | optional |
| remediation_notes | text | optional |
| date_reported / date_updated / date_resolved | datetime | server-managed |
