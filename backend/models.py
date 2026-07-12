# created models.py file
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

ITEM_TYPES = ("Bug", "Vulnerability", "Feature Request")
SEVERITIES = ("Critical", "High", "Medium", "Low", "Informational")
STATUSES = ("Open", "In Progress", "Resolved", "Closed", "Won't Fix")

DEFAULT_COMPANY = "VULNTRACKCOMPANY"

def now_utc():
    return datetime.now(timezone.utc)

class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable= False)
    description = db.Column(db.Text, nullable=False)

    item_type = db.Column(db.String(30), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    cvss_score = db.Column(db.Float, nullable=True)
    cve_id = db.Column(db.String(30), nullable=True)

    status = db.Column(db.String(20),nullable=False, default="Open")

    affected_asset = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(150), nullable=False, default=DEFAULT_COMPANY)
    reporter = db.Column(db.String(120), nullable=False)
    assignee = db.Column(db.String(120), nullable=True)

    remediation_notes = db.Column(db.Text, nullable=True)

    date_reported = db.Column(db.DateTime, nullable=False, default=now_utc)
    date_updated = db.Column(db.DateTime, nullable= False, default=now_utc, onupdate=now_utc)
    date_resolved = db.Column(db.DateTime, nullable=True)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "item_type": self.item_type,
            "severity": self.severity,
            "cvss_score": self.cvss_score,
            "cve_id": self.cve_id,
            "status": self.status,
            "affected_asset": self.affected_asset,
            "company": self.company,
            "reporter": self.reporter,
            "assignee": self.assignee,
            "remediation_notes": self.remediation_notes,
            "date_reported": self.date_reported.isoformat() if self.date_reported else None,
            "date_updated": self.date_updated.isoformat() if self.date_updated else None,
            "date_resolved": self.date_resolved.isoformat() if self.date_resolved else None,
            }