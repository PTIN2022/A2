from utils.db import db
from models.model import Cliente, ClienteSchema
from utils.utils import encrypt_password


def get_all_clientes():
    c = Cliente.query.all()
    return ClienteSchema(many=True).dump(c)


def get_cliente_id(id):
    c = Cliente.query.filter(Cliente.id_usuari == id).one_or_none()
    return ClienteSchema().dump(c)


def get_cliente_dni(DNI):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    return ClienteSchema().dump(c)


def post_cliente(nombre, apellido, email, DNI, foto, telefono, username, password):
    password = encrypt_password(password)
    c = Cliente(nombre, apellido, email, DNI, foto, telefono, username, password)
    db.session.add(c)
    db.session.commit()
    return ClienteSchema().dump(c)


def delete_cliente_dni(DNI):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    if c:
        db.session.delete(c)
        db.session.commit()
        return True
    return False


def delete_cliente_id(id):
    c = Cliente.query.filter(Cliente.id_usuari == id).one_or_none()
    if c:
        db.session.delete(c)
        db.session.commit()
        return True
    return False
