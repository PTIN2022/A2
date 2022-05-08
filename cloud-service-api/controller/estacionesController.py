from models.estacion import Estacion, EstacionSchema
from models.plaza import Plaza, PlazaSchema
from utils.db import db


def get_all_estaciones():
    i = Estacion.query.all()
    return EstacionSchema(many=True).dump(i)


def get_estacion_by_id(id):
    i = Estacion.query.filter(Estacion.id == id).one_or_none()
    if i:
        estacion_dict = EstacionSchema().dump(i)

        estacion_dict["Cargadores"] = []
        for cargador in i.Cargadores:
            estacion_dict["Cargadores"].append(PlazaSchema().dump(cargador))

        return estacion_dict

    return None


def delete_plaza(id, id_plaza):
    i = Plaza.query.filter(Plaza.id == id_plaza).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False
