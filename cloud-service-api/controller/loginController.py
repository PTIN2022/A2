from models.trabajador import Trabajador, TrabajadorSchema
from utils.db import db


def post_login(email, password):
    try:
        t = Trabajador.query.filter(Trabajador.email == email).one_or_none()
        t = TrabajadorSchema().dump(t)
        if t['password'] == password:
            return t
    except:
        return None
