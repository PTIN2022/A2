import os
from utils.db import db
from flask import Flask
from datetime import datetime
from models.cargador import Cargador
from routes.trabajador import trabajador
from routes.estaciones import estaciones
from routes.incidencias import incidencias
from models.estacion import Estacion, EstacionSchema
from models.promocion import Promocion
from models.promocionEstacion import PromocionEstacion
from models.reserva import Reserva
from models.vehiculo import Vehiculo
from models.aviso import Aviso
from models.usuari_t import Usuari_t, Usuari_tSchema
from models.cliente import Cliente, ClienteSchema
from models.horas import Horas
from models.consumo import Consumo
from models.pago import Pago
from models.trabajador import Trabajador
from models.vehiculoCliente import VehiculoCliente


def init_db():
    db.init_app(app)
    with app.app_context():
        db.create_all()


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # TODO: Pass to mysql
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # TODO: review
app.config["TESTING"] = False

app.register_blueprint(incidencias, url_prefix='/api')
app.register_blueprint(estaciones, url_prefix='/api')
app.register_blueprint(trabajador, url_prefix='/api')

if app.config["TESTING"] is False:
    if os.path.exists("./test.db"):
        os.remove("./test.db")

    init_db()
    with app.app_context():
        e = Estacion("VG3", "mi casa", 720, 85, 23, 20, 130, "Alfredo_Manresa", 1300, 2000, "url")
        db.session.add(e)
        db.session.commit()

        p = Promocion(32, 5, 2, datetime.today(), datetime.today(), "activa", "superdecuento")
        db.session.add(p)
        db.session.commit()

        p = PromocionEstacion(e.id_estacion, p.id_promo)
        db.session.add(p)
        db.session.commit()

        u_t = Usuari_t("cliente", "sergi", "garcia", "meh@gmail.com", "245363Y", "foto_chula", 4674387249, "sergi.ib", "mehmeh123")       
        db.session.add(u_t)
        db.session.commit()
        print(Usuari_tSchema().dump(u_t))

        c = Cliente(u_t.id_usuari)
        db.session.add(c)
        db.session.commit()
        print("----------")
        print(Usuari_tSchema().dump(c))
        print(ClienteSchema().dump(c))

        t = Trabajador(u_t.id_usuari, "jefe", datetime.today(), "Activo", "Amigo de la infancia?")
        db.session.add(t)
        db.session.commit()

        print(EstacionSchema().dump(e))

        print(e)
        p1 = Cargador("activa", "algunsitio", e.id_estacion)
        p2 = Cargador("activa", "algunsitio", e.id_estacion)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()

        h1 = Horas(datetime.today(), datetime.today(), p1.id_cargador)
        h2 = Horas(datetime.today(), datetime.today(), p2.id_cargador)
        db.session.add(h1)
        db.session.add(h2)
        db.session.commit()

        co1 = Consumo(p1.id_cargador, h1.id)
        co2 = Consumo(p2.id_cargador, h2.id)
        db.session.add(co1)
        db.session.add(co2)
        db.session.commit()

        v = Vehiculo("X96392WXES", 34, 7237, "Toyota Corolla", 58)
        db.session.add(v)
        db.session.commit()

        vc = VehiculoCliente(v.id_vehiculo, c.id_cliente)
        db.session.add(vc)
        db.session.commit()

        r1 = Reserva(datetime.today(), datetime.today(), datetime.today(), datetime.today(), 25.2, 10.1, "activa", p1.id_cargador, v.id_vehiculo, c.id_cliente)
        r2 = Reserva(datetime.today(), datetime.today(), datetime.today(), datetime.today(), 50, 60, "terminada", p2.id_cargador, v.id_vehiculo, c.id_cliente)
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()

        pag1 = Pago(r1.id_reserva, c.id_cliente, "Pagado")
        pag2 = Pago(r2.id_reserva, c.id_cliente, "Pendiente")
        db.session.add(pag1)
        db.session.add(pag2)
        db.session.commit()

        a = Aviso("Cancelación", "motomamiiiiii", datetime.today(), r1.id_reserva, c.id_cliente)  # c.id_cliente
        db.session.add(a)
        db.session.commit()

if __name__ == "__main__":  # pragma: no cover
    print("=========================================")
    print("Test me on: http://ptin2022.github.io/A2/")
    print("=========================================")
    app.run(host="0.0.0.0")
