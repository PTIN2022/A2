import os
import json
from utils.db import db
from flask import Flask
from flask_mqtt import Mqtt
from datetime import datetime

from models.reserva import Reserva
from models.estacion import Estacion
from models.cargador import Cargador
from models.horas import Horas
from models.consumo import Consumo
from routes.trabajador import trabajador
from routes.soporte import soporte
from routes.estaciones import estaciones
from routes.incidencias import incidencias
from routes.clientes import clientes
from routes.reservas import reservas
from routes.estadisticas import estadisticas


def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI', "sqlite:///test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False
app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL', 'test.mosquitto.org')  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT', "1883"))  # default port for non-tls connection
app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME', '')  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD', '')  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = int(os.getenv('MQTT_KEEPALIVE', "5"))  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = os.getenv('MQTT_TLS_ENABLED', False)  # set TLS to disabled for testing purposes


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
    p1 = Cargador("cargando", "coordenada", e.id_estacion)
    p2 = Cargador("cargando", "cordenada", e.id_estacion)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    h1 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('18:00', '%H:%M').time(), 1)
    h2 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('19:00', '%H:%M').time(), 1)
    h3 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('20:00', '%H:%M').time(), 1)
    h4 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('21:00', '%H:%M').time(), 1)
    db.session.add(h1)
    db.session.add(h2)
    db.session.add(h3)
    db.session.add(h4)
    db.session.commit()
    h5 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('18:00', '%H:%M').time(), 2)
    h6 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('19:00', '%H:%M').time(), 2)
    h7 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('20:00', '%H:%M').time(), 2)
    h8 = Horas(datetime.strptime('2022-04-20', '%Y-%m-%d').date(), datetime.strptime('22:00', '%H:%M').time(), 2)
    db.session.add(h5)
    db.session.add(h6)
    db.session.add(h7)
    db.session.add(h8)
    db.session.commit()
    c1 = Consumo(p1.id_cargador, h1.id, 300,  400)
    c2 = Consumo(p1.id_cargador, h2.id, 220,  400)
    c3 = Consumo(p1.id_cargador, h3.id, 390,  400)
    c4 = Consumo(p1.id_cargador, h4.id, 120,  400)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.commit()
    c5 = Consumo(p2.id_cargador, h5.id, 111,  500)
    c6 = Consumo(p2.id_cargador, h6.id, 300,  500)
    c7 = Consumo(p2.id_cargador, h7.id, 333,  500)
    c8 = Consumo(p2.id_cargador, h8.id, 800,  500)
    db.session.add(c5)
    db.session.add(c6)
    db.session.add(c7)
    db.session.add(c8)
    db.session.commit()
    h1 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('18:00', '%H:%M').time(), 1)
    h2 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('19:00', '%H:%M').time(), 1)
    h3 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('20:00', '%H:%M').time(), 1)
    h4 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('21:00', '%H:%M').time(), 1)
    h5 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('18:00', '%H:%M').time(), 2)
    h6 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('19:00', '%H:%M').time(), 2)
    h7 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('20:00', '%H:%M').time(), 2)
    h8 = Horas(datetime.strptime('2022-04-21', '%Y-%m-%d').date(), datetime.strptime('22:00', '%H:%M').time(), 2)
    db.session.add(h1)
    db.session.add(h2)
    db.session.add(h3)
    db.session.add(h4)
    db.session.add(h5)
    db.session.add(h6)
    db.session.add(h7)
    db.session.add(h8)
    db.session.commit()
    c1 = Consumo(p1.id_cargador, h1.id, 600,  700)
    c2 = Consumo(p1.id_cargador, h2.id, 200,  700)
    c3 = Consumo(p1.id_cargador, h3.id, 116,  700)
    c4 = Consumo(p1.id_cargador, h4.id, 200,  700)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.commit()
    c5 = Consumo(p2.id_cargador, h5.id, 300,  500)
    c6 = Consumo(p2.id_cargador, h6.id, 800,  500)
    c7 = Consumo(p2.id_cargador, h7.id, 900,  500)
    c8 = Consumo(p2.id_cargador, h8.id, 300,  500)
    db.session.add(c5)
    db.session.add(c6)
    db.session.add(c7)
    db.session.add(c8)
    db.session.commit()


app.register_blueprint(incidencias, url_prefix='/api')
app.register_blueprint(estaciones, url_prefix='/api')
app.register_blueprint(trabajador, url_prefix='/api')
app.register_blueprint(clientes, url_prefix='/api')
app.register_blueprint(reservas, url_prefix='/api')
app.register_blueprint(soporte, url_prefix='/api')
app.register_blueprint(estadisticas, url_prefix='/api')

if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
