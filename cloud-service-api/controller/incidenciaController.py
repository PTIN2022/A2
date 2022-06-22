from utils.db import db
from models.model import Averia, AveriaSchema, Estacion


def get_all_incidencias():
    i = Averia.query.all()
    return AveriaSchema(many=True).dump(i)


def get_incidencias_id(id):
    i = Averia.query.filter(Averia.id_averia == id).one_or_none()
    return AveriaSchema().dump(i)


def get_incidencias_estacion(estacion):
    i = Averia.query.filter(Averia.name_estacion == estacion)
    return AveriaSchema(many=True).dump(i)


def post_incidencia(estacion, fecha, descripcion, estado=False):
    est = Estacion.query.filter(Estacion.nombre_est == estacion).one_or_none()
    if est:
        est.estado = "Dañada"
        i = Averia(fecha, estado, descripcion, estacion)
        db.session.add(i)
        db.session.commit()
        return i.id_averia
    else:
        return None


def remove_incidencia(id):
    i = Averia.query.filter(Averia.id_averia == id).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False


def modify_incidencia(id, estacion=None, fecha_averia=None, descripcion=None, estado=None, trabajador=None):
    i = Averia.query.filter(Averia.id_averia == id).one_or_none()
    if i:
        if estacion:
            i.name_estacion = estacion
        if fecha_averia:
            i.fecha = fecha_averia
        if descripcion:
            i.descripcion = descripcion
        if estado is not None:
            i.estado = estado
        if trabajador is not None:
            i.id_trabajador = trabajador

        db.session.commit()
        return AveriaSchema().dump(i)

    return None
