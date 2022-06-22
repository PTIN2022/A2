from utils.db import db
from models.model import Transaccion, Cliente


def get_all_transacciones():
    i = Transaccion.query.all()
    return TransaccionSchema(many=True).dump(i)


def post_transacciones_by_reservas(id_cliente, importe, tipo, id_reserva):
    i = Reserva.query.filter(Reserva.id_reserva == id_reserva, Reserva.id_cliente == id_cliente).one_or_none()
    if i:
        t = Transaccion(importe, tipo, id_cliente, id_reserva)
        db.session.add(t)
        db.session.commit()
        return TransaccionSchema().dump(t)
    return None


def get_transacciones_by_clientes(id_cliente):
    i = Cliente.query.filter(Cliente.id_cliente == id_cliente).one_or_none()
    if i:
        return TransaccionSchema(many=True).dump(i.transacciones)
    else:
        return None