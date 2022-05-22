from datetime import datetime
from models.promocionEstacion import PromocionEstacion, PromocionEstacionSchema
from models.promociones import Promocion, PromocionSchema
from utils.db import db


def get_all_promociones():
    p = Promocion.query.all()
    return PromocionSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promocion.query.get(id_promo)
    return PromocionSchema().dump(p)


def post_promociones(descuento, fecha_inicio_post, fecha_fin_post, estado, descripcion):
    try:
        # Pasamos a datetime las fechas
        fecha_inicio = datetime.strptime(fecha_inicio_post, '%Y-%m-%dT%H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin_post, '%Y-%m-%dT%H:%M:%S')
        p = Promocion(descuento, fecha_inicio, fecha_fin, estado, descripcion)
        db.session.add(p)
        db.session.commit()
        return PromocionSchema().dump(p)
    except (ValueError):  # noqa: E722
        return None


def modify_promociones(id_promo, descuento=None, fecha_inicio=None, fecha_fin=None, estado=False, descripcion=None):
    try:
        p = get_promo_id(id_promo)
        p = Promocion(p["descuento"], p["fecha_inicio"], p["fecha_fin"], p["estado"], p["descripcion"])
        if p:
            if descuento:
                p.descuento = descuento
            if fecha_inicio:
                p.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
            if fecha_fin:
                p.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
            if estado == "true":
                p.estado = True
            else:
                p.estado = False
            if descripcion:
                p.descripcion = descripcion
            db.session.commit()
            return PromocionSchema().dump(p)
    except (KeyError):
        return post_promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
    except (ValueError):
        return None
    return None


def delete_promocion(id_promo):
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    if p:
        db.session.delete(p)
        db.session.commit()
        return True
    return False


def get_promo_estado(estado):
    if estado == "true":
        p.estado = True
    else:
        p.estado = False
    p = Promocion.query.filter(Promocion.estado == estado).all()
    return PromocionSchema(many=True).dump(p)


def get_promo_estacion(id_electrolinera):
    p = Promocion.query.filter(PromocionEstacion.id_electrolinera == id_electrolinera)
    return PromocionSchema(many=True).dump(p)
