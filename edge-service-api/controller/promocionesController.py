from datetime import datetime
from controller import estacionesController
from models.model import Promociones, PromocionesSchema, Estacion, EstacionSchema
from utils.db import db
from utils.utils import strtobool
from flask import Blueprint, jsonify, request


def get_all_promociones():
    p = Promociones.query.all()
    return PromocionesSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promociones.query.get(id_promo)
    return PromocionesSchema().dump(p)


def post_promociones(descuento, fecha_inicio_post, fecha_fin_post, estado, descripcion):
    try:
        # Pasamos a datetime las fechas
        fecha_inicio = datetime.strptime(fecha_inicio_post, '%Y-%m-%dT%H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin_post, '%Y-%m-%dT%H:%M:%S')
        p = Promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
        db.session.add(p)
        db.session.commit()
        return PromocionesSchema().dump(p)
    except (ValueError):  # noqa: E722
        return ValueError
    return None


def modify_promociones(id_promo, descuento=None, fecha_inicio=None, fecha_fin=None, estado=False, descripcion=None):
    try:
        #p = get_promo_id(id_promo)
        #p = Promociones(id_promo,p["descuento"], p["fecha_inicio"], p["fecha_fin"], p["estado"], p["descripcion"])
        p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
        if p:
            if descuento:
                p.descuento = descuento
            if fecha_inicio:
                p.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
            if fecha_fin:
                p.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
            if estado:
                p.estado = strtobool(estado)
            if descripcion:
                p.descripcion = descripcion
            #db.session.query().filter_by(id = id_promo).update({"descuento":p["descuento"],"fecha_inicio":p["fecha_inicio"],"fecha_fin":p["fecha_fin"],"estado":p["estado"],"descrpicion":p["descripcion"]})
            db.session.commit()
            return PromocionesSchema().dump(p)
    #except (KeyError):
    #    return post_promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
    except (ValueError):
        return None
    return None


def delete_promocion(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    if p:
        db.session.delete(p)
        db.session.commit()
        return True
    return False

#Mirar estado en rama raul
def get_promo_estado(estado):
    p = Promociones.query.filter(Promociones.estado == strtobool(estado))
    return PromocionesSchema(many=True).dump(p)


def get_promo_estaciones():
    p = Estacion.query.all()
    if p:
        Lista_estaciones = EstacionSchema(many=True).dump(p)
        for estacion in Lista_estaciones:
            promociones = PromocionesSchema(many=True).dump(estacion.promociones)
        return schema
    return None


def get_promo_estacion(id_electrolinera):
    print(str(id_electrolinera))
    p = Estacion.query.filter(Estacion.id_estacion == id_electrolinera).one_or_none()
    print(str(p))
    if p:
        schema = EstacionSchema().dump(p)
        pschema = PromocionesSchema(many=True).dump(p.promociones)
        return schema
    return None
