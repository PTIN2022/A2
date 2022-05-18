from models.promocionEstacion import PromocionEstacion, PromocionEstacionSchema
from models.promocion import Promocion, PromocionSchema
from utils.db import db


def get_all_promociones(id_estacion):
    i = PromocionEstacion.query.filter(PromocionEstacion.id_estacion == id).one_or_none()
    if i:
        promociones_dict = PromocionSchema().dump(i)

#        promociones_dict["id_estacion"] = []
#        for cargador in i.Cargadors:
#            estacion_dict["id_estacion"].append(CargadorSchema().dump(cargador))

        return promociones_dict

    return []


def get_promocion_by_id(id):
    print(str(id))
    i = Promocion.query.filter(Promocion.id_promo == id)
    return PromocionSchema(many=True).dump(i)

