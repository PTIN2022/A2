import jwt
from utils.db import db
from flask import current_app as app
from datetime import datetime, timedelta
from utils.utils import encrypt_password
from models.trabajador import Trabajador, TrabajadorSchema


def expire_date(minutes):
    now = datetime.utcnow()
    new_date = now + timedelta(minutes=minutes)
    return new_date


def post_login(email, password):
    password = encrypt_password(password)
    t = Trabajador.query.filter(Trabajador.email == email).one_or_none()
    if t:
        if t.password == password:
            t.last_access = 'connected'
            db.session.commit()
            return jwt.encode({"email": t.email, "rol": t.rol, "exp": app.config['EXPIRE_TOKEN_TIME']}, app.config['SECRET_KEY'], algorithm="HS256")

    return None


def get_logout():
    return None
