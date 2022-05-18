from models.trabajador import Trabajador, TrabajadorSchema
from utils.utils import encrypt_password
from utils.db import db


def get_all_trabajadores():
    t = Trabajador.query.all()
    return TrabajadorSchema(many=True).dump(t)


def get_trabajador_dni(dni):
    t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
    return TrabajadorSchema().dump(t)


def post_trabajador(DNI, name, lastname, telf, email, rol, password, last_access, picture):
    password = encrypt_password(password)
    t = Trabajador.query.filter(Trabajador.dni == DNI).one_or_none()
    if t:
        return None

    t = Trabajador(DNI, name, lastname, telf, email, rol, password, int(last_access), picture)
    db.session.add(t)
    db.session.commit()
    return TrabajadorSchema().dump(t)


# habra que mojararlo (last_access, picture...)
def modify_trabajador(DNI, dni_change=None, name=None, lastname=None, telf=None, email=None, rol=None, picture=None, last_acces=None, password=None):
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
        if picture:
            t.picture = picture
        if dni_change:
            t.dni = dni_change
        if last_acces:
            t.last_acces = last_acces
        if password:
            password = encrypt_password(password)
            t.password = password

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
