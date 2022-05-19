from models.promocionEstacion import PromocionEstacion, PromocionEstacionSchema
from models.promocion import Promocion, PromocionSchema
from utils.db import db


def get_all_promociones(id_estacion):
    i = Promocion.query.filter(Promocion.id_promo == PromocionEstacion.id_promo).filter(PromocionEstacion.id_estacion == id_estacion).all()
    if i:
        promociones_dict = PromocionSchema().dump(i)

        promociones_dict["id_promo"] = []
        for cargador in i.id_promo:
            estacion_dict["id_promo"].append(PromocionSchema().dump(cargador))

        return promociones_dict

    return None


def get_promocion_by_id(id):
    print(str(id))
    i = Promocion.query.filter(Promocion.id_promo == id)
    return PromocionSchema(many=True).dump(i)

