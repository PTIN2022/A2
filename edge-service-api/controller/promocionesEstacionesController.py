from models.promocionEstacion import PromocionEstacion, PromocionEstacionSchema
from utils.db import db


def get_all_promociones_estaciones():
    p = PromocionEstacion.query.all()
    return PromocionEstacionSchema().dump(p)


def get_id_promociones_estaciones(id_promo):
    p = PromocionEstacion.query.get(id_promo)
    return PromocionEstacionSchema().dump(p)


def post_promociones_estaciones(id_promo, id_estacion):
    nuevaPromocionConEstacion = PromocionEstacion(int(id_estacion), int(id_promo))
    print("Param -> "+str(id_promo)+" <-> "+str(id_estacion))
    db.session.add(nuevaPromocionConEstacion)
    db.session.commit()
    print("Object -> "+str(type(nuevaPromocionConEstacion))+" <-> "+str(nuevaPromocionConEstacion))
    return PromocionEstacionSchema().dump(nuevaPromocionConEstacion)


def get_id_estaciones_promociones(id_estacion):
    p = PromocionEstacion.query.get(id_estacion)
    return PromocionEstacionSchema().dump(p)


