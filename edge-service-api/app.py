import os
import time
from utils.db import db
from flask import Flask
from routes.reservas import reservas
from routes.estaciones import estaciones
from utils.fake_data import fakedata
from multiprocessing import Lock


def init_db():
    time.sleep(5)
    db.init_app(app)
    with app.app_context():
        #db.drop_all()  # TODO: REMOVE AT THE END OF THE PROYECT
        db.create_all()


lock = Lock()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False

app.register_blueprint(reservas, url_prefix="/api")
app.register_blueprint(estaciones, url_prefix="/api")

if os.path.exists("./test.db"):
    os.remove("./test.db")

lock.acquire()

try:
    init_db()
    #with app.app_context():
    #    fakedata()

finally:
    lock.release()


if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
