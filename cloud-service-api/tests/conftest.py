import os
import pytest

from app import app, init_db


@pytest.fixture(scope='module')
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/pytest.db"
    app.config["TESTING"] = True

    if os.path.exists("/tmp/pytest.db"):
        os.remove("/tmp/pytest.db")

    with app.test_client() as client:
        init_db()
        yield client

