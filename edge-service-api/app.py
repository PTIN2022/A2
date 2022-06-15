import os
import time
from utils.db import db
from flask import Flask
from routes.reservas import reservas
from routes.estaciones import estaciones
<<<<<<< HEAD
from routes.promocionesEstaciones import promocionesEstaciones
from routes.promociones import promociones
from models.cargador import Cargador
from models.estacion import Estacion
=======
from routes.clientes import clientes
from utils.fake_data import fakedata
from multiprocessing import Lock

insert = bool(os.getenv('INSERT_FAKER', False))
>>>>>>> 7249b1eaa51d404b2f5e7cb9d0826ac4ad115c8a


def init_db():
    time.sleep(5)
    db.init_app(app)
    with app.app_context():
        if insert:
            db.drop_all()
        db.create_all()

        if insert:
            fakedata()


lock = Lock()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False

<<<<<<< HEAD
app.register_blueprint(reservas)
app.register_blueprint(estaciones)
app.register_blueprint(promociones)
app.register_blueprint(promocionesEstaciones)
=======
app.register_blueprint(reservas, url_prefix="/api")
app.register_blueprint(estaciones, url_prefix="/api")
app.register_blueprint(clientes, url_prefix="/api")
>>>>>>> 7249b1eaa51d404b2f5e7cb9d0826ac4ad115c8a

if insert:
    if os.path.exists("./test.db"):
        os.remove("./test.db")

lock.acquire()
try:
    init_db()
finally:
    lock.release()

<<<<<<< HEAD
    print(e)
    p1 = Cargador("cargando", "coordenada", e.id_estacion)
    p2 = Cargador("cargando", "coordenada", e.id_estacion)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
=======
>>>>>>> 7249b1eaa51d404b2f5e7cb9d0826ac4ad115c8a

if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")

    if not insert:
        app.run(host="0.0.0.0")
