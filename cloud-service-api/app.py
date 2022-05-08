import os
from utils.db import db
from flask import Flask
from models.plaza import Plaza
from routes.trabajador import trabajador
from routes.soporte import soporte
from models.chat import Chat
from routes.estaciones import estaciones
from routes.incidencias import incidencias
from models.estacion import Estacion


def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # TODO: Pass to mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False


app.register_blueprint(incidencias)
app.register_blueprint(estaciones)
app.register_blueprint(trabajador)
app.register_blueprint(soporte)


if app.config["TESTING"] is False:
    if os.path.exists("./test.db"):
        os.remove("./test.db")

    init_db()
    with app.app_context():
        e = Estacion("VG3", "mi casa", 720, 85, 23, 20, 130, "Alfredo_Manresa", 1300, 2000, "url")
        db.session.add(e)
        db.session.commit()

        print(e)
        p1 = Plaza(23, 23, 23, "mario", e.id)
        p2 = Plaza(30, 23, 40, "mario", e.id)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()


if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
