import os
from utils.db import db
from flask import Flask
from models.plaza import Plaza
from routes.trabajador import trabajador
from routes.estaciones import estaciones
from routes.incidencias import incidencias
from models.estacion import Estacion
from routes.login import login, logout
import jwt


def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # TODO: Pass to mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False

# secrets.token_hex(32) TODO: regenerate with a real secret on the server
app.config['SECRET_KEY']='bf9d91da2b703c30e770279ee82b17692def66a956b25b7c2d92f4088dfea293'

# salt = os.urandom(32) TODO: regenerate with a real secret on the servers
app.config['SALT']='\xd2\x1f\xca\x0c\xc5\xe6:)\xa9\xeb<\x07j\r\xb6\xef\xda$\xb8\xc5XJak\xab\x9d\x0e\x99\xaf\xc7\x94\xba'.encode("utf-8")
app.config["EXPIRE_TOKEN_TIME"] = 2*60  # mins



app.register_blueprint(incidencias)
app.register_blueprint(estaciones)
app.register_blueprint(trabajador)
app.register_blueprint(login)
app.register_blueprint(logout)

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
