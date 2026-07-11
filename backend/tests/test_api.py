#tests

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
    os.unlink()
HEADERS = {"X-API-KEY": API_KEY, "Content_Type": "application/json"}

