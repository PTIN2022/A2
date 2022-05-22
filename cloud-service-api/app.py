import os
import json
import string
import random

from utils.db import db
from flask import Flask
from flask_mqtt import Mqtt
from datetime import datetime

from models.model import *
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


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # TODO: Pass to mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes

app.register_blueprint(incidencias, url_prefix='/api')
app.register_blueprint(estaciones, url_prefix='/api')
app.register_blueprint(trabajador, url_prefix='/api')
app.register_blueprint(clientes, url_prefix='/api')
app.register_blueprint(reservas, url_prefix='/api')
app.register_blueprint(soporte, url_prefix='/api')
app.register_blueprint(estadisticas, url_prefix='/api')

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
    e = Estacion("VG3", 720, 85, 32, "Rambla de L'exposicio",20,"Zona industrial", 12,130,
                "+347624872487", "Vilanova i la geltru", "España")  # , t.id_trabajador
    db.session.add(e)
    db.session.commit()

    p1 = Cargador("cargando", 1, "fast" ,e.id_estacion)
    p2 = Cargador("cargando", 2, "meh" ,e.id_estacion)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()
    h1 = Horas(datetime.strptime('2022-04-20 11:00', '%Y-%m-%d %H:%M'))
    h2 = Horas(datetime.strptime('2022-04-20 12:00', '%Y-%m-%d %H:%M'))
    h3 = Horas(datetime.strptime('2022-04-20 13:00', '%Y-%m-%d %H:%M'))
    h4 = Horas(datetime.strptime('2022-04-20 14:00', '%Y-%m-%d %H:%M'))
    h5 = Horas(datetime.strptime('2022-04-21 11:00', '%Y-%m-%d %H:%M'))
    h6 = Horas(datetime.strptime('2022-04-21 12:00', '%Y-%m-%d %H:%M'))
    h7 = Horas(datetime.strptime('2022-04-21 13:00', '%Y-%m-%d %H:%M'))
    h8 = Horas(datetime.strptime('2022-04-21 14:00', '%Y-%m-%d %H:%M'))
    db.session.add(h1)
    db.session.add(h2)
    db.session.add(h3)
    db.session.add(h4)
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
    c1 = Consumo(p2.id_cargador, h1.id, 111,  500)
    c2 = Consumo(p2.id_cargador, h2.id, 300,  500)
    c3 = Consumo(p2.id_cargador, h3.id, 333,  500)
    c4 = Consumo(p2.id_cargador, h4.id, 800,  500)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.commit()
    c1 = Consumo(p2.id_cargador, h7.id, 111,  500)
    c2 = Consumo(p2.id_cargador, h8.id, 300,  500)
    c3 = Consumo(p2.id_cargador, h6.id, 333,  500)
    c4 = Consumo(p2.id_cargador, h5.id, 800,  500)
    db.session.add(c1)
    db.session.add(c2)
    db.session.add(c3)
    db.session.add(c4)
    db.session.commit()

    t = Trabajador("otrosergi", "garcia", "meh@gmail.com", "245363Y", "foto_chula", 4674387249, "sergi.ib", "mehmeh123", "jefe", "Activo", datetime.today(), "Amigo de la infancia?", e.id_estacion)
    db.session.add(t)
    db.session.commit()

    c = Cliente("clientesergi", "garcia", "meh@gmail.com", "245363Y", "foto_chula", 4674387249, "sergi.ib", "mehmeh123")
    db.session.add(c)
    db.session.commit()
    #e.encargado = t.id_trabajador
    #db.session.commit()


    p = Promociones(32, 2, datetime.today(), datetime.today(), "activa", "superdecuento")
    db.session.add(p)
    db.session.commit()

    p.estaciones.append(e)
    db.session.commit()
    p1 = Cargador("ocupado", 2, "tipo C", e.id_estacion)
    p2 = Cargador("libre", 5, "super fast", e.id_estacion)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

    model_list = ["500e Cabrio eléctrico", "Taycan eléctrico","e-tron GT eléctrico", "Leaf eléctrico", "Ioniq eléctrico", "i3 eléctrico", "ID.3 eléctrico", "2 eléctrico", "UX300e eléctrico", "EV6 eléctrico"]
    
    mod = Modelo(model_list[0], "Fiat", False, 42)
    db.session.add(mod)
    mod2 = Modelo(model_list[1], "Porsche", True, 93.4)
    db.session.add(mod2)
    mod3 = Modelo(model_list[2], "Audi", True, 93.4)
    db.session.add(mod3)
    mod4 = Modelo(model_list[3], "Nissan", False, 42.6)
    db.session.add(mod4)
    mod5 = Modelo(model_list[4], "Hyundai", False, 72.6)
    db.session.add(mod5)
    mod6 = Modelo(model_list[5], "BMW", False, 42.2)
    db.session.add(mod6)
    mod7 = Modelo(model_list[6], "Volkswagen", True, 77)
    db.session.add(mod7)
    mod8 = Modelo(model_list[7], "Polestar", False, 69)
    db.session.add(mod8)
    mod9 = Modelo(model_list[8], "Lexus", False, 54.3)
    db.session.add(mod9)
    mod10 = Modelo(model_list[9], "Kia", True, 77)
    db.session.add(mod10)
    db.session.commit()

    for i in range(50):
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))
        numeros = ''.join(random.choices(string.digits, k=4))
        matricula = ''.join(random.choices(letras+numeros, k=7))
        procentaje_bat = random.randint(0, 100)
        modelo = random.choice(model_list)

        v = Vehiculo(matricula, procentaje_bat, modelo)
        db.session.add(v)

    #v = Vehiculo("X96392WXES", 34, mod.modelo)
    #db.session.add(v)
    db.session.commit()
#####
    c.vehiculos.append(v)
    db.session.commit()

    r1 = Reserva(datetime.today(), datetime.today(), 50, 25.2,10.1, True, 90.99, True,True,p1.id_cargador, v.matricula, c.id_cliente)
    r2 = Reserva(datetime.today(), datetime.today(), 33, 50, 60,
                 False, 44.44, True,True,p2.id_cargador, v.matricula, c.id_cliente)
    db.session.add(r1)
    db.session.add(r2)
    db.session.commit()

    a = Aviso("Cancelación","motomamiiiiii",datetime.today(), r1.id_reserva, c.id_cliente)#c.id_cliente
    db.session.add(a)
    db.session.commit()

    ticket = Ticket(datetime.today(), "Error App",
                    "No me deja reservar en la estacion de Rambla Exposicio, no se que le pasa", "Pendiente", c.id_cliente)
    db.session.add(ticket)
    db.session.commit()

    m = Mensaje("Me parece que lo haceis todo mal, salu2",datetime.today(),
                c.id_usuari, ticket.id_ticket)
    db.session.add(m)
    db.session.commit()

    av = Averia(datetime.today(), "Pendiente",
                    "No funciona la estación por mantenimiento", t.id_trabajador, e.id_estacion)
    db.session.add(av)
    db.session.commit()

    s = Sesiones(datetime.today(), datetime.today(), t.id_trabajador)
    db.session.add(s)
    db.session.commit()


if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
