import os
import pytest
from routes.reservas import reservas  # noqa: F401
from routes.estaciones import estaciones  # noqa: F401
from models.cargador import Cargador  # noqa: F401
from models.estacion import Estacion  # noqa: F401

from utils.db import db
from app import app, init_db


@pytest.fixture(scope='module')
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/pytest.db"
    app.config["TESTING"] = True

    if os.path.exists("/tmp/pytest.db"):
        os.remove("/tmp/pytest.db")

    with app.test_client() as client:
        init_db()
        with app.app_context():
            e = Estacion("VG3", "mi casa", 720, 85, 23, 20, 130, "Alfredo_Manresa", 1300, 2000, "url")
            db.session.add(e)
            db.session.commit()

            print(e)
            p1 = Cargador("cargando", "coordenada", e.id_estacion)
            p2 = Cargador("cargadon", "cordenada", e.id_estacion)
            db.session.add(p1)
            db.session.add(p2)
            db.session.commit()
        yield client
