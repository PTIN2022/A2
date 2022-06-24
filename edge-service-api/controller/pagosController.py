from utils.db import db
from models.model import Transaccion, Reserva, TransaccionSchema, Historial
from datetime import datetime

def get_all_transacciones():
    i = Transaccion.query.all()
    return TransaccionSchema(many=True).dump(i)


def post_transacciones_by_reservas(cliente, importe, tipo, id_reserva):
    i = Reserva.query.filter(Reserva.id_reserva == id_reserva, Reserva.id_cliente == cliente.id_cliente).one_or_none()
    if i:
        t = Transaccion.query.filter(Transaccion.id_reserva == id_reserva).one_or_none()
        if t is None:
            t = Transaccion(importe, tipo, id_reserva, cliente.id_cliente)
            cliente.transacciones.append(t)
            db.session.add(t)
            db.session.commit()
            return TransaccionSchema().dump(t)
        return 0
    return None


def get_transacciones_by_clientes(cliente):
    if cliente:
        return TransaccionSchema(many=True).dump(cliente.transacciones)
    else:
        return None

def put_saldo_and_create_historial(cliente, type, saldo):
    if str(type) == "add":
        cliente.saldo += saldo
    elif cliente.saldo >= saldo:
        cliente.saldo -= saldo
    else:
        return False
    db.session.commit()
    h = Historial(datetime.now(),cliente.id_cliente, cliente.saldo, type)
    cliente.historial.append(h)
    db.session.add(h)
    db.session.commit()
    return True
