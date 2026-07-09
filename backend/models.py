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
    