import os
import pytest

os.environ["MQTT_BROKER_URL"] = "test.mosquitto.org"
os.environ["MQTT_BROKER_PORT"] = "1883"

from app import app, init_db  # noqa: E402


@pytest.fixture(scope='module')
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/pytest.db"
    app.config["TESTING"] = True

    if os.path.exists("/tmp/pytest.db"):
        os.remove("/tmp/pytest.db")

    with app.test_client() as client:
        init_db()
        yield client
