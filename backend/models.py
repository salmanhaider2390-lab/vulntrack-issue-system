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
    cve_id = db.Column(db.String(30, nullable=True))

    status = db.Column(db.String(20),nullable=False, default="Open")

def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "item_type": self.item_type,
            "severity" : self.severity,
            "cvss_score" : self.cvss_score,
            "cve_id" : self.cve_id,
            "status" : self.status,
        }