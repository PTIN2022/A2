from utils.db import db
from models.model import *


def get_all_trabajadores():
    t = Trabajador.query.all()
    return TrabajadorSchema(many=True).dump(t)


def get_trabajador_dni(dni):
    t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
    return TrabajadorSchema().dump(t)


def post_trabajador(DNI, name, lastname, telf, email, rol, last_access, picture):
    t = Trabajador(DNI, name, lastname, telf, email, rol, int(last_access), picture)
    db.session.add(t)
    db.session.commit()
    return TrabajadorSchema().dump(t)


# habra que mojararlo (last_access, picture...)
def modify_trabajador(DNI, dni_change=None, name=None, lastname=None, telf=None, email=None, rol=None, last_access=None, picture=None):
    t = Trabajador.query.filter(Trabajador.dni == DNI).one_or_none()
    if t:
        if name:
            t.name = name
        if lastname:
            t.lastname = lastname
        if telf:
            t.telf = telf
        if email:
            t.email = email
        if rol:
            t.rol = rol
        if last_access:
            t.last_access = last_access
        if picture:
            t.picture = picture
        if dni_change:
            t.dni = dni_change

        db.session.commit()
        return TrabajadorSchema().dump(t)

    return None


def delete_trabajador(dni):
    t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
    if t:
        db.session.delete(t)
        db.session.commit()
        return True
    return False
