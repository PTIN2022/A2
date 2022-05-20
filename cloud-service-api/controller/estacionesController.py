from models.estacion import Estacion, EstacionSchema
from models.cargador import Cargador, CargadorSchema
from utils.db import db


def get_all_estaciones():
    i = Estacion.query.all()
    return EstacionSchema(many=True).dump(i)


def get_estacion_by_id(id):
    i = Estacion.query.filter(Estacion.id_estacion == id).one_or_none()
    if i:
        estacion_dict = EstacionSchema().dump(i)

        estacion_dict["cargadores"] = []
        for cargador in i.cargadores:
            estacion_dict["cargadores"].append(CargadorSchema().dump(cargador))

        return estacion_dict

    return None


def get_estacion_by_coor(lat_str=0, long_str=0):
    lat = float(lat_str)
    long = float(long_str)
    lista_estaciones = {}
    coor = Estacion.query.with_entities(Estacion.latitud, Estacion.longitud).order_by(db.desc(Estacion.latitud)).all()
    if coor:
        points = []
        lista_estaciones["Estaciones"] = []
        for i in range(len(coor)):
            tupla = [coor[i][0], coor[i][1]]
            points.append(tupla)
        lista_order = get_ordered_list(points, lat, long)
        valor = 5
        if len(lista_order) < 5:
            valor = len(lista_order)
        for i in range(valor):
            est = Estacion.query.filter(Estacion.latitud == lista_order[i][0], Estacion.longitud == lista_order[i][1]).one_or_none()
            est_obj = get_estacion_by_id(est.id_estacion)
            lista_estaciones["Estaciones"].append(est_obj)
    return lista_estaciones


def get_ordered_list(points, x, y):
    points.sort(key=lambda p: (p[0] - x)**2 + (p[1] - y)**2)
    return points
