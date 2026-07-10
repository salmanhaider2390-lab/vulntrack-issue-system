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

