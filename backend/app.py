import os
from functools import wraps

from flask import Flask, request, jsonify
from flask_cors import CORS

from models import db, Issue, ITEM_TYPES, SEVERITIES, STATUSES, DEFAULT_COMPANY, now_utc
from validation import validate_issue_payload

API_KEY = os.environ.get("VULNTRACK_API_KEY", "vuln-track-sa121417")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(db_path=None):
    app = Flask(__name__)
    CORS(app)

    db_path = db_path or os.path.join(BASE_DIR, "vulntrack.db")
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
            return jsonify({"error": "Unauthorized. Missing or invalid X-API-Key."}), 401
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

    # ---------- CREATE ----------
    @app.post("/api/issues")
    @require_api_key
    def create_issue():
        data = request.get_json(silent=True) or {}
        errors, cleaned = validate_issue_payload(data, partial=False)
        if errors:
            return jsonify({"errors": errors}), 400

        issue = Issue(
            title=cleaned["title"],
            description=cleaned["description"],
            item_type=cleaned["item_type"],
            severity=cleaned["severity"],
            cvss_score=cleaned.get("cvss_score"),
            cve_id=cleaned.get("cve_id"),
            status=cleaned.get("status", "Open"),
            affected_asset=cleaned["affected_asset"],
            company=cleaned.get("company") or DEFAULT_COMPANY,
            reporter=cleaned["reporter"],
            assignee=cleaned.get("assignee"),
            remediation_notes=cleaned.get("remediation_notes"),
        )

        db.session.add(issue)
        db.session.commit()
        return jsonify(issue.to_dict()), 201

    # ---------- READ ----------
    @app.get("/api/issues")
    def list_issues():
        query = Issue.query

        q = request.args.get("q")
        if q:
            like = f"%{q}%"
            query = query.filter(db.or_(Issue.title.ilike(like), Issue.description.ilike(like)))

        for field, column in [
            ("status", Issue.status),
            ("severity", Issue.severity),
            ("item_type", Issue.item_type),
            ("company", Issue.company),
            ("assignee", Issue.assignee),
        ]:
            val = request.args.get(field)
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
        col = sortable.get(sort_by, Issue.date_reported)
        query = query.order_by(col.desc() if order == "desc" else col.asc())

        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return jsonify({
            "total": total,
            "page": page,
            "per_page": per_page,
            "items": [i.to_dict() for i in items],
        })

    @app.get("/api/issues/<int:issue_id>")
    def get_issue(issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return jsonify({"error": "Issue not found."}), 404
        return jsonify(issue.to_dict())

    # ---------- UPDATE ----------
    @app.put("/api/issues/<int:issue_id>")
    @require_api_key
    def update_issue(issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return jsonify({"error": "Issue not found."}), 404

        data = request.get_json(silent=True) or {}
        errors, cleaned = validate_issue_payload(data, partial=False)
        if errors:
            return jsonify({"errors": errors}), 400

        _apply_changes(issue, cleaned)
        db.session.commit()
        return jsonify(issue.to_dict())

    @app.patch("/api/issues/<int:issue_id>")
    @require_api_key
    def patch_issue(issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return jsonify({"error": "Issue not found."}), 404

        data = request.get_json(silent=True) or {}
        errors, cleaned = validate_issue_payload(data, partial=True)
        if errors:
            return jsonify({"errors": errors}), 400

        _apply_changes(issue, cleaned)
        db.session.commit()
        return jsonify(issue.to_dict())

    def _apply_changes(issue, cleaned):
        for field, new_value in cleaned.items():
            setattr(issue, field, new_value)
        if cleaned.get("status") == "Resolved" and not issue.date_resolved:
            issue.date_resolved = now_utc()
        issue.date_updated = now_utc()

    # ---------- DELETE ----------
    @app.delete("/api/issues/<int:issue_id>")
    @require_api_key
    def delete_issue(issue_id):
        issue = db.session.get(Issue, issue_id)
        if not issue:
            return jsonify({"error": "Issue not found."}), 404
        db.session.delete(issue)
        db.session.commit()
        return jsonify({"message": f"Issue {issue_id} deleted."})


if __name__ == "__main__":
    application = create_app()
    application.run(debug=True, port=5000)
    