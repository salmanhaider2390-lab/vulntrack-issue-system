# Issue &amp; Vulnerability Tracking System — VulnTrack Company

Backend: **Flask** + **Flask-SQLAlchemy** + **SQLite**. Frontend: a lightweight **vanilla HTML/JS** webpage

---

## 1. Requirements

### 1.1 Purpose
Track software issues, bugs, feature requests, and security vulnerabilities affecting
VulnTrack Company' systems, with enough structure to report vulnerabilities and remediation tracking

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

## 2. Project structure

```
vulntrack/
├── backend/
│   ├── app.py           # Flask app, routes
│   ├── models.py        # SQLAlchemy model (Issue)
│   ├── validation.py     # request payload validation
│   ├── seed_data.py      # demo data inputs
│   └── tests/
│       └── test_api.py   # pytest
├── frontend/
│   └── index.html        
├── .gitignore
└── README.md
```

## 3. Running it

```bash
cd backend
python -m venv venv && source venv/bin/activate 

# start the API (http://127.0.0.1:5000)
python app.py

# in a second terminal: load demo data
python seed_data.py

# run tests
python -m pytest tests/ -v
```

Then open `frontend/index.html` directly in a browser (or serve it with
`python -m http.server` from the `frontend/` folder). It talks to the API at
`http://127.0.0.1:5000/api` and uses the default dev API key
(`vuln-track-sa121417`, matching `VULNTRACK_API_KEY` in `app.py`)

### Postman
Import the base URL `http://127.0.0.1:5000/api` and set header
`X-API-Key: vuln-track-sa121417` on any write request (POST/PUT/PATCH/DELETE).
Example bodies are in `backend/seed_data.py`.

## 4. Testing

17 automated tests (`pytest`) cover: health check, auth enforcement, create with
valid/invalid payloads (missing fields, bad CVSS, bad CVE format, missing CVSS on
a Vulnerability), read (single/list/404), search, filter, sort, full update,
partial update (status→Resolved auto-stamps `date_resolved`), delete, summary
reporting, and CSV export. Run with:

```bash
python -m pytest backend/tests/ -v
```


## 5. Source control workflow

This project was developed with incremental commits on GitHub, each attributed
to its origin per the assignment's academic integrity requirement:

- `self` — code written from scratch
- `library` — third-party dependency usage (Flask, Flask-SQLAlchemy, Flask-Cors)
  used per their documented public APIs
- `ai` — sections created with AI assistance, reviewed and adapted

## 6. Code attribution 

| Component | Origin | Notes |
|---|---|---|
| `models.py` (data model) | self| Schema designed|
| `validation.py` | self / ai-assisted | Custom validation logic; drafted with AI assistance |
| `app.py` (routes) | self| Core CRUD + reporting logic;|
| `tests/test_api.py` | self / ai-assisted | Test cases created with AI assistance |
| `frontend/index.html` | self / ai-assisted | Vanilla JS client; created with AI assistance |
| Flask, Flask-SQLAlchemy, Flask-Cors, pytest | library | Third-party packages, used under their respective licences (BSD/MIT) via PyPI, no source code copied |
