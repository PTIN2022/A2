from datetime import datetime
from controller import estacionesController
from models.model import Promociones, PromocionesSchema
from utils.db import db


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
        p = get_promo_id(id_promo)
        p = Promociones(p["descuento"], p["fecha_inicio"], p["fecha_fin"], p["estado"], p["descripcion"])
        if p:
            if descuento:
                p.descuento = descuento
            if fecha_inicio:
                p.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
            if fecha_fin:
                p.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
            if estado == 'true':
                p.estado = True
            else:
                p.estado = False
            if descripcion:
                p.descripcion = descripcion
            db.session.commit()
            return PromocionesSchema().dump(p)
    except (KeyError):
        return post_promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
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


def get_promo_estado(estado):
    p = Promociones.query.filter(Promociones.estado == estado).all()
    return PromocionesSchema(many=True).dump(p)


def get_promo_estaciones():
    p = estacionesController.get_all_estaciones()
    for estacion in p:
        print("Estacion.ID_estacion: "+str(estacion["id_estacion"]))
        ep = promocionesEstaciones.get_promociones_estaciones()

    return ep


def get_promo_estacion(id_electrolinera):
    p = Promociones.query.filter(PromocionesEstacion.id_electrolinera == id_electrolinera)
    return PromocionesSchema(many=True).dump(p)
