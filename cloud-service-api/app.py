import os
import json
from utils.db import db
from flask import Flask
from flask_mqtt import Mqtt
from datetime import datetime

from models.reserva import Reserva
from models.estacion import Estacion
from models.cargador import Cargador
from routes.trabajador import trabajador
from routes.estaciones import estaciones
from routes.incidencias import incidencias
from routes.reservas import reservas


def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # TODO: Pass to mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False

app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

mqtt = Mqtt(app)
mqtt.subscribe('estacion/#')


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("aseasdfgs")
    mqtt.subscribe('estacion/#')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(data)
    print(data["payload"])
    print(type(data["payload"]))
    with app.app_context():
        data = json.loads(data["payload"])
        ini = datetime.strptime(data["fecha_entrada"], '%Y-%m-%dT%H:%M:%S')
        fin = datetime.strptime(data["fecha_salida"], '%Y-%m-%dT%H:%M:%S')
        r = Reserva(ini, fin, data["id_cargador"], data["id_vehiculo"], data["id_cliente"])
        db.session.add(r)
        db.session.commit()

    # TODO: pasarlo a otro fichero


if os.path.exists("./test.db"):
    os.remove("./test.db")

init_db()
with app.app_context():
    e = Estacion("VG3", "mi casa", 720, 85, 23, 20, 130, "Alfredo_Manresa", 1300, 2000, "url")
    db.session.add(e)
    db.session.commit()

    print(e)
    p1 = Cargador("cargando", "coordenada", e.id_estacion)
    p2 = Cargador("cargando", "cordenada", e.id_estacion)
    db.session.add(p1)
    db.session.add(p2)
    r1 = Reserva(datetime.strptime("2022-04-18T11:00:00", '%Y-%m-%dT%H:%M:%S') , datetime.strptime("2022-04-18T18:00:00", '%Y-%m-%dT%H:%M:%S'), 1, "LKE2378", "1238712N", 55.0, datetime.strptime("2022-04-18T01:00:00", '%Y-%m-%dT%H:%M:%S'))
    db.session.add(r1)
    db.session.commit()

app.register_blueprint(incidencias, url_prefix='/api')
app.register_blueprint(estaciones, url_prefix='/api')
app.register_blueprint(trabajador, url_prefix='/api')
app.register_blueprint(reservas, url_prefix='/api')

if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
