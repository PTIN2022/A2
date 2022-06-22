from models.model import Estacion, EstacionSchema, CargadorSchema, PromocionesSchema
from utils.db import db
from math import radians, cos, sin, asin, sqrt


def get_all_estaciones():
    i = Estacion.query.all()
    return EstacionSchema(many=True).dump(i)


def get_estacion_by_id(id):
    i = Estacion.query.filter(Estacion.id_estacion == id).one_or_none()
    if i:
        estacion_dict = EstacionSchema().dump(i)
        estacion_dict["Cargadores"] = CargadorSchema(many=True).dump(i.cargadores)
        estacion_dict["Promoción activa"] = []
        if i.promociones:
            for promocion in i.promociones:
                if promocion.estado:
                    estacion_dict["Promoción activa"] = PromocionesSchema().dump(promocion)
        return estacion_dict
    return None


def get_estacion_by_coor(lat_str=0, long_str=0, ratio=0):
    lat = float(lat_str)
    long = float(long_str)
    lista_estaciones = {}
    coor = Estacion.query.with_entities(Estacion.latitud, Estacion.longitud, Estacion.id_estacion).order_by(db.desc(Estacion.latitud)).all()
    if coor:
        points = []
        lista_estaciones["Estaciones"] = []
        for i in range(len(coor)):
            tupla = [coor[i][0], coor[i][1], coor[i][2]]
            points.append(tupla)
        lista_order = get_ordered_list(points, lat, long, ratio)
        for i in lista_order:
            print(i)
        for i in range(len(lista_order)):
            i = Estacion.query.filter(Estacion.id_estacion == coor[i][2]).one_or_none()  # TODO: esto esta bien?
            est_obj = EstacionSchema().dump(i)
            if est_obj:
                lista_estaciones["Estaciones"].append(est_obj)
    return lista_estaciones


def get_ordered_list(points, x, y, ratio):
    points.sort(key=lambda p: (p[0] - x)**2 + (p[1] - y)**2)
    points_ratio = []
    for point in points:
        print(point)
        distance = haversine(x, y, point[0], point[1])
        print(distance)
        if int(ratio) >= distance:
            points_ratio.append(point)
        else:
            break
    return points_ratio


def haversine(lat1, lon1, lat2, lon2):
    R = 6372.8
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    return R * c
