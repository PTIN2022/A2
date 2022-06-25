
from models.model import Promociones, PromocionesSchema, PromocionEstacion, PromocionEstacionSchema, Estacion, EstacionSchema
from utils.db import db
from datetime import datetime


def get_all_promociones():
    p = Promociones.query.all()
    return PromocionesSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    return PromocionesSchema().dump(p)


def get_promo_estado(estado):
    promos = []
    result = []
    relation = PromocionEstacion.query.filter(PromocionEstacion.estado == estado)
    for i in relation:
        if not int(i.id_promo) in promos:
            promos.append(int(i.id_promo))
    for promo in promos:
        p = Promociones.query.filter(Promociones.id_promo == promo)
        result.append(PromocionesSchema(many=True).dump(p))
    return result


def get_promo_estacion(id_estacion):
    promos = []
    result = []
    relation = PromocionEstacion.query.filter(PromocionEstacion.id_estacion == id_estacion)
    for i in relation:
        if not i.id_promo in result:
            promos.append(i.id_promo)
    for promo in promos:
        p = Promociones.query.filter(Promociones.id_promo == promo)
        result.append(PromocionesSchema(many=True).dump(p))
    return result


def get_promo_estaciones(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    if p:
        result = []
        relation = PromocionEstacion.query.filter(PromocionEstacion.id_promo == p.id_promo)
        for i in relation:
            if not i.id_estacion in result:
                result.append(i.id_estacion)
        return result
    else:
        return None


def post_promociones(estaciones, descuento, fecha_inicio, fecha_fin, descripcion):
    # Pasamos a datetime las fechas y creamos promo
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
    p = Promociones(descuento, 0, fecha_inicio, fecha_fin, descripcion)
    db.session.add(p)
    db.session.commit()
    # añadimos las estaciones
    for estacion in estaciones:
        relation = PromocionEstacion(estacion, p.id_promo, 'inactiva')
        db.session.add(relation)
        db.session.commit()
    return PromocionesSchema().dump(p)


def modify_promociones(id_promo, id_estacion=None, descuento=None, fecha_inicio=None, fecha_fin=None, descripcion=None, cantidad_usados=None):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    if p:
        relation = PromocionEstacion.query.filter(PromocionEstacion.id_promo == p.id_promo, PromocionEstacion.id_estacion == id_estacion).one_or_none()
        if not relation:
            relation = PromocionEstacion(id_estacion, p.id_promo, 'inactiva')
            db.session.add(relation)
            db.session.commit()
        if descuento:
            p.descuento = descuento
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
            p.fecha_inicio = fecha_inicio
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
            p.fecha_fin = fecha_fin
        if descripcion:
            p.descripcion = descripcion
        if cantidad_usados:
            p.cantidad_usados = cantidad_usados
        db.session.commit()
        return PromocionesSchema().dump(p)
    return None


def modify_estado(id_promo, id_estacion):
    relation = PromocionEstacion.query.filter(PromocionEstacion.id_promo == id_promo, PromocionEstacion.id_estacion == id_estacion).one_or_none()
    if relation:
            promos = PromocionEstacion.query.filter(PromocionEstacion.id_estacion == id_estacion)
            for i in promos:
                i.estado = 'inactiva'
                db.session.commit()
            relation.estado = 'activa'
            db.session.commit()
            return True
    else:
        return None


def delete_promocion(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    relation = PromocionEstacion.query.filter(PromocionEstacion.id_promo == id_promo)
    if p:
        for i in relation:
            db.session.delete(i)
            db.session.commit()
        db.session.delete(p)
        db.session.commit()
        return True
    return False


def delete_estacion_promocion(id_promo, id_estacion):
    relation = PromocionEstacion.query.filter(PromocionEstacion.id_promo == id_promo, PromocionEstacion.id_estacion == id_estacion).one_or_none()
    if relation:
        db.session.delete(relation)
        db.session.commit()
        return True
    return False
