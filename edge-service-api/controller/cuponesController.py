from utils.db import db
from models.model import Cupon, CuponSchema, Cliente


def get_cupones_user(id_user):
    cupon_list = Cupon.query.filter(Cupon.id_cliente == id_user).all()
    return CuponSchema(many=True).dump(cupon_list)


def add_cupon_user(descuento, cupon, id_user):
    c = Cupon.query.filter(Cupon.cupon == cupon).one_or_none()
    if c:
        return {"error": "Este cupon ya existe. Usa otro nombre."}

    u = Cliente.query.filter(Cliente.id_usuari == id_user)
    if u:
        c = Cupon(descuento, cupon, id_user)
        db.session.add(c)
        db.session.commit()
        return CuponSchema().dump(c)
    else:
        return {"error": "Este usuario no existe"}


def set_cupon_estado(cupon, estado):
    c = Cupon.query.filter(Cupon.cupon == cupon).one_or_none()
    if c:
        c.estado = estado
        db.session.commit()
        return CuponSchema().dump(c)
    else:
        return {"error": "Este cupon no existe"}


def check_cupon_user(id_cupon, id_user):
    cupon_list = Cupon.query.filter(Cupon.id_cliente == id_user, Cupon.cupon == id_cupon).one_or_none()
    if cupon_list:
        return CuponSchema().dump(cupon_list)

    return {"error": "Este usuario no tiene este cupon."}
