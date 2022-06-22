from utils.db import db
from models.model import Aviso, AvisoSchema, Reserva


def get_all_avisos():
    i = Aviso.query.all()
    return AvisoSchema(many=True).dump(i)


def post_avisos(id_cliente, id_reserva, tipo, texto, fecha):
    i = Reserva.query.filter(Reserva.id_reserva == id_reserva, Reserva.id_cliente == id_cliente).one_or_none()
    if i:
        a = Aviso(tipo, texto, fecha, id_reserva, id_cliente)
        db.session.add(a)
        db.session.commit()
        return AvisoSchema().dump(a)
    return None


def get_avisos_by_reserva(id_cliente, id_reserva):
    a = Aviso.query.filter(Aviso.id_cliente == id_cliente, Aviso.id_reserva == id_reserva)
    if a:
        return AvisoSchema(many=True).dump(a)
    else:
        return None


def delete_aviso(id_cliente, id_aviso):
    a = Aviso.query.filter(Aviso.id_aviso == id_aviso, Aviso.id_cliente == id_cliente).one_or_none()
    if a:
        db.session.delete(a)
        db.session.commit()
        return True
    else:
        return None
