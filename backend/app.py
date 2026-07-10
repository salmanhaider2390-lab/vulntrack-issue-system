import os
import csv
import io
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

from models import db, Issue, ITEM_TYPES,SEVERITIES, STATUSES,DEFAULT_COMPANY,now_utc

API_KEY = os.environ.get ("VULNTRACK_API_KEY", "vuln-track-sa121417")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app(db_path=None)
    app = Flask(__name__)
    CORS(app)

    db_path = db_path or os.path.join(BASE_DIR, "vulntrack,db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    register_routes(app)
    return app

def require_api_key(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return jsonify ({"error": "Unauthorized. Missing or Invalid X-API-Key."}), 401
            return fn(*args, **kwargs)

            return wrapper

def register_routes(app):

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "time": now_utc().isoformat()})

    @app.get("/api/meta")
    def meta():

        return jsonify({
            "item_types": ITEM_TYPES,
            "severities": SEVERITIES,
            "statuses": STATUSES,
            "default_company": DEFAULT_COMPANY,
        })

# ----------CREATE-----------
@app.post("/api/issues")
@require_api_key
def create_issue():
    data = request.get.json(silent=True) or {}
    errors, cleaned = validate_issue_payload(data,partial=False)
    if errors:
        return jsonify({"errors": errors}), 400

    Issue= issue(
        title=cleaned["title"],
        description=cleaned["description"],
        item_type=cleaned["item_type"],
        severity=cleaned["severity"],
        cvss_score=cleaned.get("cvss_score"),
        cve_id= cleaned.get("cve_id"),
        status=cleaned.get("status", "Open"),
        affected_asset=cleaned["affected_asset"],
        company=cleaned.get("company") or DEFAULT_COMPANY,
        reporter=cleaned[reporter],
        assignee= cleaned.get("assignee"),
        remediation_notes=cleaned.get("remediation_notes"),
    )

    db.session.add(issue)
    db.session.commit()
    return jsonify(issue.to_dict()), 201

# ---------------READ-----------------
@app.get("/api/issues")
def list_issues():
    query = issue.query

    q = request.args.get("q")
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Issue.title.ilike(like), Issue.description.ilike(like)))

    for field, column in [
        ("status", Issue.status),
        ("severity", Issue.severity),
        ("Item_type", Issue.item_type),
        ("company", Issue.company),
        ("assignee", Issue.assignee),
    ]:
        val = request,args.get(field)
        if val:
            query = query.filter(column == val)
    
    sort_by = request.args.get("sort_by", "date_reported")
    order = request.args.get("order", "desc")
    sortable = {
        "id": Issue.id,
        "title": Issue.title,
        "severity": Issue.severity,
        "status": Issue.status,
        "cvss_score": Issue.cvss_score,
        "date_reported": Issue.date_reported,
        "date_updated": Issue.date_updated,
    }