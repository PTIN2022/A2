from models.model import Promociones, PromocionesSchema
from utils.db import db
from utils.utils import strtobool
from datetime import datetime


def get_all_promociones():
    p = Promociones.query.all()
    return PromocionesSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    
    return PromocionesSchema().dump(p)


def modify_promociones(id_promo, descuento=None, fecha_inicio=None, fecha_fin=None, estado=None, descripcion=None):
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
    if p:
        if descuento:
            p.descuento = descuento
        if fecha_inicio:
            p.fecha_inicio = fecha_inicio
        if fecha_fin:
            p.fecha_fin = fecha_fin
        if estado:
            p.estado = estado
        if descripcion:
            p.descripcion = descripcion
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
