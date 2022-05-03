from utils.db import db
from models.reserva import Reserva, ReservaSchema


def get_all_reservas():
    i = Reserva.query.all()
    return ReservaSchema(many=True).dump(i)


def get_reservas_id(id):
    i = Reserva.query.filter(Reserva.id == id).one_or_none()
    return ReservaSchema().dump(i)


def get_reservas_estacion(estacion):
    # TODO: pillar todos los cargadores de la estacion
    # TODO: enviar json con horas ocupadas apartir de ahora, 
    i = Reserva.query.filter(Reserva.id_estacion == estacion)
    return ReservaSchema(many=True).dump(i)


def get_reservas_matricula(matricula):
    i = Reserva.query.filter(Reserva.matricula == matricula)
    return ReservaSchema(many=True).dump(i)


def get_reservas_dni(dni):
    i = Reserva.query.filter(Reserva.DNI == dni)
    return ReservaSchema(many=True).dump(i)


def post_reserva(id_estacion, desde, hasta, matricula, data_inicio, data_final, DNI):
    # TODO: Get cargadores de una estacion
    # TODO: ver disponibilidad de esos cargadores en desde hasta
    # TODO: de los disponibles crear una reserva
    # Gardar reserva
    i = Reserva(id_estacion, desde, hasta, matricula, data, DNI)
    db.session.add(i)
    db.session.commit()
    # TODO: Push reserva al cloud
    return i.id


def remove_reserva(id):
    i = Reserva.query.filter(Reserva.id == id).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False


def modify_reserva(id, id_estacion=None, desde=None, hasta=None, matricula=None, data=None, DNI=None):
    i = Reserva.query.filter(Reserva.id == id).one_or_none()
    if i:
        if id_estacion:
            i.id_estacion = id_estacion
        if desde:
            i.desde = desde
        if hasta:
            i.hasta = hasta
        if matricula:
            i.matricula = matricula
        if data:
            i.data = data
        if DNI:
            i.DNI = DNI

        db.session.commit()
        return ReservaSchema().dump(i)

    return None
