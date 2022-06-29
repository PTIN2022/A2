from utils.db import db
from utils.utils import encrypt_password
from utils.mqtt_utils import send_to_edge
from models.model import Trabajador, TrabajadorSchema, Estacion


def get_all_trabajadores():
    t = Trabajador.query.all()
    return TrabajadorSchema(many=True).dump(t)


def get_trabajador_dni(dni):
    t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
    return TrabajadorSchema().dump(t)


def post_trabajador(nombre, apellido, email, dni, foto, telefono, username, password, cargo, estado, last_access, question, id_estacion):
    e = Estacion.query.filter(Estacion.nombre_est == id_estacion).one_or_none()
    if e:
        password = encrypt_password(password)
        t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
        if t:
            return {"error": "Trabajador already exists."}
        t = Trabajador(nombre, apellido, email, dni, foto, telefono, username, password, cargo, estado, last_access, question, e.id_estacion)
        db.session.add(t)
        db.session.commit()
        tv = TrabajadorSchema().dump(t)
        tv["password"] = t.password
        tv["id_estacion"] = e.id_estacion
        send_to_edge("gesys/edge/trabajador", tv)
        return TrabajadorSchema().dump(t)

    return {"error": "Estacion does not exists."}


# habra que mojararlo (last_access, picture...)
def modify_trabajador(dni, nombre, apellido, email, dni_change, foto, telefono, username, password, cargo, estado, question, id_estacion):
    t = Trabajador.query.filter(Trabajador.dni == dni).one_or_none()
    if t:
        if nombre:
            t.nombre = nombre
        if apellido:
            t.apellido = apellido
        if email:
            t.email = email
        if dni_change:
            t.dni = dni_change
        if foto:
            t.foto = foto
        if telefono:
            t.telefono = telefono
        if username:
            t.username = username
        if password:
            password = encrypt_password(password)
            t.password = password
        if cargo:
            t.cargo = cargo
        if estado:
            t.estado = estado
        if question:
            t.question = question
        if id_estacion:
            e = Estacion.query.filter(Estacion.nombre_est == id_estacion).one_or_none()
            if (e):
                t.id_estacion = e.id_estacion

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
