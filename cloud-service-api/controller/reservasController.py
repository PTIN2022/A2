from utils.db import db
from models.reservas import Reserva, ReservaSchema


def get_all_reservas():
    i = Reserva.query.all()
    return ReservaSchema(many=True).dump(i)


def get_reservas_estacion(estacion):
    i = Reserva.query.filter(Reserva.estacion == estacion)
    return ReservaSchema(many=True).dump(i)


def get_reservas_matricula(matricula):
    i = Reserva.query.filter(Reserva.matricula == matricula)
    return ReservaSchema(many=True).dump(i)


def get_reservas_dni(dni):
    i = Reserva.query.filter(Reserva.DNI == dni)
    return ReservaSchema(many=True).dump(i)


def get_reservas_id(id_reserva):
    i = Reserva.query.filter(Reserva.id_reserva == id_reserva).one_or_none()
    return ReservaSchema().dump(i)


def remove_reserva(id_reserva):
    i = Reserva.query.filter(Reserva.id_reserva == id_reserva).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False
