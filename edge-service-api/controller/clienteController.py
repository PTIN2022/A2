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


def modify_cliente(dni, nombre, apellido, email, foto, telefono, username, password, saldo):
    t = Cliente.query.filter(Cliente.dni == dni).one_or_none()
    if t:
        if nombre:
            t.nombre = nombre
        if apellido:
            t.apellido = apellido
        if email:
            t.email = email
        if foto:
            t.foto = foto
        if telefono:
            t.telefono = telefono
        if username:
            t.username = username
        if password:
            password = encrypt_password(password)
            t.password = password
        if saldo:
            t.saldo = saldo
        db.session.commit()
        return ClienteSchema().dump(t)

    return None
