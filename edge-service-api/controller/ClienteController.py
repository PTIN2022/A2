from models.cliente import Cliente, ClienteSchema
from models.reserva import Reserva, ReservaSchema
from utils.db import db
from sqlalchemy.inspection import inspect


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


def get_cliente_reservas(DNI):
    r = Reserva.query.filter(Reserva.id_cliente == DNI).all()
    return ReservaSchema(many=True).dump(r)

def modify_cliente(nombre, apellido, email, DNI, foto, telefono):
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
        if foto:
            c.foto = foto

        db.session.commit()
        return ClienteSchema().dump(c)

    return None


def modify_password(DNI, last_password, new_password):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    if c:
        if c.password == last_password:
            c.password = new_password
            db.session.commit()
            return True
        else:
            return False
    else:
        return False

def delete_cliente_dni(DNI):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    if c:
        db.session.delete(c)
        db.session.commit()
        return True
    return False
