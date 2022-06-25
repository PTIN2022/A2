from utils.db import db
from models.model import Transaccion, Reserva, TransaccionSchema


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
        print(cliente.transacciones)
        return TransaccionSchema(many=True).dump(cliente.transacciones)
    else:
        return None
