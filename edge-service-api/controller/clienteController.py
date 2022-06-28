from utils.db import db
from models.model import Cliente, ClienteSchema
from utils.utils import encrypt_password
from utils.mqtt_utils import send_to_cloud

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
    cs = ClienteSchema().dump(c)
    cs["password"] = c.password
    send_to_cloud("gesys/cloud/clientes", cs)
    return ClienteSchema().dump(c)


def delete_cliente_dni(DNI):
    c = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
    if c:
        db.session.delete(c)
        db.session.commit()
        send_to_cloud("gesys/cloud/clientes/remove", {"dni": DNI})
        return True
    return False


def delete_cliente_id(id):
    c = Cliente.query.filter(Cliente.id_usuari == id).one_or_none()
    if c:
        DNI = c.dni
        db.session.delete(c)
        db.session.commit()
        send_to_cloud("gesys/cloud/clientes/remove", {"dni": DNI})
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

        cs = ClienteSchema().dump(t)
        cs["password"] = t.password
        send_to_cloud("gesys/cloud/clientes/edit", cs)
        return ClienteSchema().dump(t)

    return None
