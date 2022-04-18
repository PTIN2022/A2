import pytest

from main import app
from flask import url_for


@pytest.fixture
def client():
    app.config.update({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_get_all_incidencias(client):
    response = client.get("/incidencias")
    assert response.status_code == 200

    assert response.json == True
