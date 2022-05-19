from models.promocion import Promocion, PromocionSchema
from utils.db import db
from datetime import datetime


def get_all_promociones():
    p = Promocion.query.all()
    return PromocionSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    return PromocionSchema().dump(p)


def get_promo_estado(estado):
    if estado == 'true':
        estado = True
    else:
        estado = False
    p = Promocion.query.filter(Promocion.estado == estado)
    return PromocionSchema(many=True).dump(p)


def post_promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion):
    try:
        if estado == 'true':
            estado = True
        else:
            estado = False
        # Pasamos a datetime las fechas
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
        p = Promocion(descuento, fecha_inicio, fecha_fin, estado, descripcion)
        db.session.add(p)
        db.session.commit()
        return PromocionSchema().dump(p)
    except:
        return None


def modify_promociones(id_promo, descuento=None, fecha_inicio=None, fecha_fin=None, estado=None, descripcion=None):
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    if p:
        if descuento:
            p.descuento = descuento
        if fecha_inicio:
            p.fecha_inicio = fecha_inicio
        if fecha_fin:
            p.fecha_fin = fecha_fin
        if estado:
            if estado == 'true':
                estado = True
            else:
                estado = False
            p.estado = estado
        if descripcion:
            p.descripcion = descripcion
       

        db.session.commit()
        return PromocionSchema().dump(p)

    return None


def delete_promocion(id_promo):
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    if p:
        db.session.delete(p)
        db.session.commit()
        return True
    return False
