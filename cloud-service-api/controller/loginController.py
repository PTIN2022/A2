from models.trabajador import Trabajador, TrabajadorSchema
from utils.db import db


def post_login(email, password):
    try:
        t = Trabajador.query.filter(Trabajador.email == email).one_or_none()
        result = TrabajadorSchema().dump(t)
        if result['password'] == password:
            t.last_access = 'connected'
            db.session.commit()
            return result
    except:
        return None


def get_logout():
    return None
