from models.trabajador import Trabajador, trabajador_schema
from utils.db import db


def get_all_trabajadores():
    t = Trabajador.query.all()
    return trabajador_schema.dumps(t)


def get_trabajador_dni(dni):
    t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
    return t.to_dict()


def post_trabajador(DNI, name, lastname, telf, email, rol, last_access, picture):
    t = Trabajador(DNI, name, lastname, telf, email, rol, int(last_access), picture)
    db.session.add(t)
    db.session.commit()
    return t.to_dict()


# habra que mojararlo (last_access, picture...)
def modify_trabajador(DNI, name=None, lastname=None, telf=None, email=None, rol=None, last_access=None, picture=None):
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
    return None


def delete_trabajador(dni):
    t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
    if t:
        db.session.delete(t)
        db.session.commit()
        return True
    return False
