from utils.db import db
from models.model import Estacion, EstacionSchema, CargadorSchema, Cargador


def get_all_estaciones():
    i = Estacion.query.all()
    return EstacionSchema(many=True).dump(i)


def get_estacion_by_id(id):
    i = Estacion.query.filter(Estacion.id_estacion == id).one_or_none()
    if i:
        estacion_dict = EstacionSchema().dump(i)

        estacion_dict["Cargadores"] = CargadorSchema(many=True).dump(i.cargadores)
        return estacion_dict

    return None


def put_estacion_by_id(id, latitud=None, longitud=None, capacidad=None, direccion=None, estado=None, telefono=None, potencia_contratada=None, potencia_usada=None, potencia_actual=None, zona=None):
    i = Estacion.query.filter(Estacion.id_estacion == id).one_or_none()
    if i:
        if latitud:
            i.latitud = latitud
        if longitud:
            i.longitud = longitud
        if capacidad:
            i.capacidad = capacidad
        if direccion:
            i.direccion = direccion
        if estado:
            i.estado = estado
        if telefono:
            i.telefono = telefono
        if potencia_contratada:
            i.potencia_contratada = potencia_contratada
        if potencia_usada:
            i.potencia_usada = potencia_usada
        if potencia_actual:
            i.potencia_actual = potencia_actual
        if zona:
            i.zona = zona
        db.session.commit()
        return EstacionSchema().dump(i)

    return None


# Este no se yo si vale la pena mantenerlo
def delete_plaza(id, id_plaza):
    i = Cargador.query.filter(Cargador.id_cargador == id_plaza).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False
