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

### 1.3 Functional requirements
- **Create** new issues/vulnerabilities via `POST /api/issues`
- **Read** — single item (`GET /api/issues/<id>`) and list with **search** (`q`),
  **filter** (status/severity/type/company/assignee), **sort** (`sort_by`, `order`)
  and **pagination** (`page`, `per_page`) via `GET /api/issues`
- **Update** — full replace (`PUT`) or partial (`PATCH`, e.g. status-only change)
- **Delete** — `DELETE /api/issues/<id>`
- **Validation** — required fields, enum membership, CVSS range, CVE regex,
  business rule that vulnerabilities need a CVSS score
- **Integrity** — enforced via required fields, enum validation, CVSS range checks,
  CVE format checks, and non-null database constraints
- **Security** — write endpoints (`POST`/`PUT`/`PATCH`/`DELETE`) require an
  `X-API-Key` header (see `require_api_key` in `app.py`). Read endpoints are open,
  matching a typical internal dashboard model.

### 1.4 Non-functional
- API-first design (REST/JSON) so any client (Postman, curl, the bundled web
  frontend, or a future mobile app) can consume it
- SQLite for coursework simplicity; `SQLALCHEMY_DATABASE_URI` can be swapped for
  Postgres/MySQL with no code changes elsewhere
- CORS enabled so the frontend (served separately) can call the API

---