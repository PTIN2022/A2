import os
from utils.db import db
from flask import Flask
from routes.reservas import reservas
from routes.estaciones import estaciones
from routes.promociones import promociones
from models.cargador import Cargador
from models.estacion import Estacion
from models.promocion import Promocion
from models.promocionEstacion import PromocionEstacion

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
app.register_blueprint(promociones)

if os.path.exists("./test.db"):
    os.remove("./test.db")

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

if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
