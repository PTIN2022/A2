from utils.db import db
from models.incidencia import Incidencia, IncidenciaSchema


def get_all_incidencias():
    i = Incidencia.query.all()
    return IncidenciaSchema(many=True).dump(i)


def get_incidencias_id(id):
    i = Incidencia.query.filter(Incidencia.id == id).one_or_none()
    return IncidenciaSchema().dump(i)


def get_incidencias_estacion(estacion):
    i = Incidencia.query.filter(Incidencia.id_estacion == estacion)
    return IncidenciaSchema(many=True).dump(i)


def post_incidencia(estacion, direccion, fecha, descripcion, estado=False):
    i = Incidencia(estacion, fecha, estado, descripcion)
    db.session.add(i)
    db.session.commit()
    return i.id


def remove_incidencia(id):
    i = Incidencia.query.filter(Incidencia.id == id).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False


def modify_incidencia(id, estacion=None, direccion=None, fecha_averia=None, descripcion=None, estado=None):
    i = Incidencia.query.filter(Incidencia.id == id).one_or_none()
    if i:
        if estacion:
            i.estacion = estacion
        if fecha_averia:
            i.fecha_averia = fecha_averia
        if descripcion:
            i.descripcion = descripcion
        if estado is not None:
            i.estado = estado

        db.session.commit()
        return IncidenciaSchema().dump(i)

    return None
