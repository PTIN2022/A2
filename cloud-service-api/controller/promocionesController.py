from models.promocion import Promocion, PromocionSchema
from models.promocionEstacion import PromocionEstacion, PromocionEstacionSchema
from utils.db import db
from datetime import datetime


def get_all_promociones():
    p = Promocion.query.all()
    p1 = PromocionEstacion.query.all()
    return PromocionSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    return PromocionSchema().dump(p)


def get_promo_estacion(id_estacion):
    p = PromocionEstacion.query.filter(PromocionEstacion.id_estacion == id_estacion)
    print(PromocionEstacionSchema(many=True).dumps(p))
    return PromocionEstacionSchema(many=True).dump(p)
	

def get_promo_estado(estado):
    p = Promocion.query.filter(Promocion.estado == estado)
    return PromocionSchema(many=True).dump(p)


def post_promociones(descuento, cantidad_cupones, cantidad_usados, fecha_inicio, fecha_fin, estado, id_estacion, descripcion):
    try:
        # Pasamos a datetime las fechas
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
        p = Promocion(descuento, cantidad_cupones, cantidad_usados, fecha_inicio, fecha_fin, estado, descripcion)
        db.session.add(p)
        db.session.commit()
        p1 = PromocionEstacion(id_estacion, p.id_promo)
        db.session.add(p1)
        db.session.commit()
        return PromocionSchema().dump(p)
    except:
        return None


# habra que mojararlo (last_access, picture...)
def modify_promociones(id_promo, descuento=None, cantidad_cupones=None, cantidad_usados=None, fecha_inicio=None, fecha_fin=None, estado=None, id_estacion=None, descripcion=None):
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    if p:
        if id_estacion:
        	p1 = PromocionEstacion.query.filter(PromocionEstacion.id_promo == id_promo).one_or_none()
        	p1.id_estacion = id_estacion
        
        if descuento:
            p.descuento = descuento
        if cantidad_cupones:
        	p.cantidad_cupones = cantidad_cupones
        if cantidad_usados:
        	p.cantidad_usados = cantidad_usados 
        if fecha_inicio:
            p.fecha_inicio = fecha_inicio
        if fecha_fin:
            p.fecha_fin = fecha_fin
        if estado:
            p.estado = estado
        if descripcion:
            p.descripcion = descripcion
       

        db.session.commit()
        return PromocionSchema().dump(p)

    return None


def delete_promocion(id_promo):
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    p1 = PromocionEstacion.query.filter(Promocion.id_promo == id_promo).one_or_none()
    if p:
        db.session.delete(p)
        db.session.commit()
        db.session.delete(p1)
        db.session.commit()
        return True
    return False
