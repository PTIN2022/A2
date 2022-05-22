from models.cliente import Cliente, ClienteSchema
from utils.db import db


def get_all_clientes():
    c = Cliente.query.all()
    return ClienteSchema(many=True).dump(c)


def get_cliente_dni(DNI):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    return ClienteSchema().dump(c)


def post_cliente(nombre, apellido, email, DNI, foto, telefono, username, password):
    c = Cliente(nombre, apellido, email, DNI, foto, telefono, username, password)
    db.session.add(c)
    db.session.commit()
    return ClienteSchema().dump(c)


def modify_cliente(nombre, apellido, email, DNI, foto, telefono, username, password):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    if c:
        if nombre:
            c.nombre = nombre
        if apellido:
            c.apellido = apellido
        if telefono:
            c.telefono = telefono
        if email:
            c.email = email
        if username:
            c.username = username
        if password:
            c.password = password
        if foto:
            c.foto = foto

        db.session.commit()
        return ClienteSchema().dump(c)

    return None

def delete_cliente_dni(DNI):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    if c:
        db.session.delete(c)
        db.session.commit()
        return True
    return False
