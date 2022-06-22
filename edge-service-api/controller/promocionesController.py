from datetime import datetime
<<<<<<< HEAD
from models.model import Promociones, PromocionesSchema, Estacion, EstacionSchema
=======
<<<<<<< HEAD
from models.promocionEstacion import PromocionEstacion, PromocionEstacionSchema
from models.promociones import Promocion, PromocionSchema
=======
from controller import estacionesController
from models.model import Promociones, PromocionesSchema
>>>>>>> 2022-5-14-xavier-app-promociones
>>>>>>> main
from utils.db import db
from utils.utils import strtobool


def get_all_promociones():
<<<<<<< HEAD
    p = Promocion.query.all()
    return PromocionSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promocion.query.get(id_promo)
    return PromocionSchema().dump(p)
=======
    p = Promociones.query.all()
    return PromocionesSchema(many=True).dump(p)


def get_promo_id(id_promo):
    p = Promociones.query.get(id_promo)
    return PromocionesSchema().dump(p)
>>>>>>> 2022-5-14-xavier-app-promociones


def post_promociones(descuento, fecha_inicio_post, fecha_fin_post, estado, descripcion):
    try:
        # Pasamos a datetime las fechas
<<<<<<< HEAD
        if estado == 'true':
            estado = True
        else:
            estado = False
        fecha_inicio = datetime.strptime(fecha_inicio_post, '%Y-%m-%dT%H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin_post, '%Y-%m-%dT%H:%M:%S')
        p = Promocion(descuento, fecha_inicio, fecha_fin, estado, descripcion)
        db.session.add(p)
        db.session.commit()
        return PromocionSchema().dump(p)
    except (ValueError):  # noqa: E722
        return None
=======
        fecha_inicio = datetime.strptime(fecha_inicio_post, '%Y-%m-%dT%H:%M:%S')
        fecha_fin = datetime.strptime(fecha_fin_post, '%Y-%m-%dT%H:%M:%S')
        p = Promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
        db.session.add(p)
        db.session.commit()
        return PromocionesSchema().dump(p)
    except (ValueError):  # noqa: E722
        return ValueError
    return None
>>>>>>> 2022-5-14-xavier-app-promociones


def modify_promociones(id_promo, descuento=None, fecha_inicio=None, fecha_fin=None, estado=False, descripcion=None):
    try:
<<<<<<< HEAD
        p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
=======
        p = get_promo_id(id_promo)
<<<<<<< HEAD
        p = Promocion(p["descuento"], p["fecha_inicio"], p["fecha_fin"], p["estado"], p["descripcion"])
=======
        p = Promociones(p["descuento"], p["fecha_inicio"], p["fecha_fin"], p["estado"], p["descripcion"])
>>>>>>> 2022-5-14-xavier-app-promociones
>>>>>>> main
        if p:
            if descuento:
                p.descuento = descuento
            if fecha_inicio:
                p.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M:%S')
            if fecha_fin:
                p.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M:%S')
            if estado:
                p.estado = strtobool(estado)
            if descripcion:
                p.descripcion = descripcion
            db.session.commit()
<<<<<<< HEAD
            return PromocionSchema().dump(p)
=======
            return PromocionesSchema().dump(p)
<<<<<<< HEAD
=======
>>>>>>> 2022-5-14-xavier-app-promociones
    except (KeyError):
        return post_promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
>>>>>>> main
    except (ValueError):
        return None
    return None


def delete_promocion(id_promo):
<<<<<<< HEAD
    p = Promocion.query.filter(Promocion.id_promo == id_promo).one_or_none()
=======
    p = Promociones.query.filter(Promociones.id_promo == id_promo).one_or_none()
>>>>>>> 2022-5-14-xavier-app-promociones
    if p:
        db.session.delete(p)
        db.session.commit()
        return True
    return False


def get_promo_estado(estado):
<<<<<<< HEAD
    p = Promociones.query.filter(Promociones.estado == strtobool(estado))
=======
<<<<<<< HEAD
    p = Promocion.query.filter(Promocion.estado == estado)
    return PromocionSchema(many=True).dump(p)


def get_promo_estacion(id_electrolinera):
    p = Promocion.query.filter(PromocionEstacion.id_electrolinera == id_electrolinera)
    return PromocionSchema(many=True).dump(p)
=======
    p = Promociones.query.filter(Promociones.estado == estado).all()
>>>>>>> main
    return PromocionesSchema(many=True).dump(p)


def get_promo_estaciones():
    lista_estaciones = Estacion.query.all()
    if lista_estaciones:
        estacion_with_promos = []
        for estacion in lista_estaciones:
            estacion_dict = EstacionSchema().dump(estacion)
            promociones = PromocionesSchema(many=True).dump(estacion.promociones)
            estacion_dict["promociones"] = promociones
            estacion_with_promos.append(estacion_dict)
        return estacion_with_promos
    return None


def get_promo_estacion(id_electrolinera):
<<<<<<< HEAD
    p = Estacion.query.filter(Estacion.id_estacion == id_electrolinera).one_or_none()
    if p:
        schema = EstacionSchema().dump(p)
        pschema = PromocionesSchema(many=True).dump(p.promociones)
        schema["promociones"] = pschema
        return schema
    return None
=======
    p = Promociones.query.filter(PromocionesEstacion.id_electrolinera == id_electrolinera)
    return PromocionesSchema(many=True).dump(p)
>>>>>>> 2022-5-14-xavier-app-promociones
>>>>>>> main
