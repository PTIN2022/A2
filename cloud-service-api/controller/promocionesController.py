from models.model import Promociones, PromocionesSchema, Estacion, EstacionSchema
from utils.db import db
from datetime import datetime


def get_all_promociones():
    p = Promociones.query.all()
    return PromocionesSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    return PromocionesSchema().dump(p)


def get_promo_estado(estado):
    p = Promociones.query.filter(Promociones.estado == estado)
    return PromocionesSchema(many=True).dump(p)


def get_promo_estaciones(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    if p:
        a = p.estaciones
        return EstacionSchema(many=True).dump(a)
    else:
        return None


def get_promo_estacion(id_estacion):
    # lista vacia donde estaran las promos que pertence a la estacion con id == id_estacion
    respuesta = []
    p = Promociones.query.all()
    for promo in p:
        a = promo.estaciones
        estac = EstacionSchema(many=True).dump(a)
        for i in estac:
            if int(i["id_estacion"]) == int(id_estacion):
                # añadimos a la lista la promo si coinciden los id
                respuesta += [PromocionesSchema().dump(promo)]
    return respuesta


def post_promociones(id_estacion, descuento, fecha_inicio, fecha_fin, estado, descripcion):
    # Comprobamos existencias estacion
    i = Estacion.query.filter(Estacion.id_estacion == id_estacion).one_or_none()
    if i:
        # Pasamos a datetime las fechas
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
        p = Promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
        db.session.add(p)
        db.session.commit()
        p.estaciones.append(i)
        db.session.commit()
        return PromocionesSchema().dump(p)
    else:
    	return None


def modify_promociones(id_promo, id_estacion=None, descuento=None, fecha_inicio=None, fecha_fin=None, estado=None, descripcion=None, cantidad_usados=None):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    if p:
        i = Estacion.query.filter(Estacion.id_estacion == id_estacion).one_or_none()
        if i:
            p.estaciones.append(i)
            db.session.commit()
        if descuento:
            p.descuento = descuento
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
            p.fecha_inicio = fecha_inicio
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
            p.fecha_fin = fecha_fin
        if estado:
            p.estado = estado
        if descripcion:
            p.descripcion = descripcion
        if cantidad_usados:
            p.cantidad_usados = cantidad_usados
        db.session.commit()
        return PromocionesSchema().dump(p)
    return None


def delete_promocion(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    if p:
        db.session.delete(p)
        db.session.commit()
        return True
    return False
