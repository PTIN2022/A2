import os
import time
import json


from utils.db import db
from utils.fake_data_static import fakedata
from flask import Flask
from flask_cors import CORS
from flask_mqtt import Mqtt
from datetime import datetime
from multiprocessing import Lock

from models.model import Reserva
from routes.trabajador import trabajador
from routes.soporte import soporte
from routes.estaciones import estaciones
from routes.incidencias import incidencias
from routes.clientes import clientes
from routes.reservas import reservas
from routes.promociones import promociones
from routes.estadisticas import estadisticas
from routes.login import login, logout


def init_db():
    time.sleep(5)
    db.init_app(app)
    with app.app_context():
        insert = bool(os.getenv('INSERT_FAKER', False))
        if insert:
            db.drop_all()
        db.create_all()

        if insert:
            fakedata()


app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False
app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL', 'test.mosquitto.org')  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT', "1883"))  # default port for non-tls connection
app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME', '')  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD', '')  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = int(os.getenv('MQTT_KEEPALIVE', "5"))  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = os.getenv('MQTT_TLS_ENABLED', False)  # set TLS to disabled for testing purposes
app.config["ON_TEST"] = bool(os.getenv('ON_TEST', False))
# secrets.token_hex(32) TODO: regenerate with a real secret on the server
app.config['SECRET_KEY'] = 'bf9d91da2b703c30e770279ee82b17692def66a956b25b7c2d92f4088dfea293'

# salt = os.urandom(32) TODO: regenerate with a real secret on the servers
app.config['SALT'] = '\xd2\x1f\xca\x0c\xc5\xe6:)\xa9\xeb<\x07j\r\xb6\xef\xda$\xb8\xc5XJak\xab\x9d\x0e\x99\xaf\xc7\x94\xba'.encode("utf-8")
app.config["EXPIRE_TOKEN_TIME"] = 2*60  # mins

print(app.config["SQLALCHEMY_DATABASE_URI"])

app.register_blueprint(incidencias, url_prefix='/api')
app.register_blueprint(estaciones, url_prefix='/api')
app.register_blueprint(trabajador, url_prefix='/api')
app.register_blueprint(clientes, url_prefix='/api')
app.register_blueprint(reservas, url_prefix='/api')
app.register_blueprint(promociones, url_prefix='/api')
app.register_blueprint(soporte, url_prefix='/api')
app.register_blueprint(estadisticas, url_prefix='/api')
app.register_blueprint(login, url_prefix='/api')
app.register_blueprint(logout, url_prefix='/api')

lock = Lock()
mqtt = Mqtt(app)
mqtt.subscribe('gesys/cloud/#')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('gesys/cloud/#')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data["payload"])
    with app.app_context():
        data = json.loads(data["payload"])
        ini = datetime.strptime(data["fecha_entrada"], '%Y-%m-%dT%H:%M:%S')
        fin = datetime.strptime(data["fecha_salida"], '%Y-%m-%dT%H:%M:%S')
        r = Reserva(ini, fin, data["procetnaje_carga"], data["precio_carga_completa"], data["precio_carga_actual"], data["estado"], data["tarifa"], data["asistida"], data["estado_pago"], data["id_cargador"], data["id_vehiculo"], data["id_cliente"])
        db.session.add(r)
        db.session.commit()

#     # TODO: pasarlo a otro fichero


# if os.path.exists("./test.db"):
#     os.remove("./test.db")


lock.acquire()
try:
    init_db()
finally:
    lock.release()


if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")

    insert = bool(os.getenv('INSERT_FAKER', False))
    if not insert:
        app.run(host="0.0.0.0")
