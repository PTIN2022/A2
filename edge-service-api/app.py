import os
from utils.db import db
from flask import Flask
from routes.reservas import reservas
from routes.estaciones import estaciones
from models.cargador import Cargador
from models.estacion import Estacion
from random import randint
import random


def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # TODO: Pass to mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False

app.register_blueprint(reservas)
app.register_blueprint(estaciones)

if os.path.exists("./test.db"):
    os.remove("./test.db")

init_db()
with app.app_context():
    e = Estacion("VG30", 12.000, 13.0000, 32, "mi casa", 720, 3, 23, 130, 690389157, "España", "Vilanova")
    db.session.add(e)
    db.session.commit()
    p1 = Cargador(True, 11, e.id_estacion)
    p2 = Cargador(False, 10, e.id_estacion)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    for i in range(30):
        nombre_est = "VG" + str(i)
        pot = randint(300, 900)
        plazas_oc = randint(0, 23)
        potencia_cons = randint(0, pot)
        zona = randint(1, 5)
        lat = random.uniform(1.1, 80.1)
        long = random.uniform(1.1, 90.1)
        e1 = Estacion(nombre_est, lat, long, 32, "mi casa", pot, zona, plazas_oc, potencia_cons, 690389157, "España", "Vilanova")
        db.session.add(e1)
        db.session.commit()


if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
