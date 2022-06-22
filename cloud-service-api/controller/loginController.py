import jwt
from utils.db import db
from flask import current_app as app
from datetime import datetime, timedelta
from utils.utils import encrypt_password
from models.model import Trabajador


def expire_date(minutes):
    now = datetime.utcnow()
    new_date = now + timedelta(minutes=minutes)
    return new_date


def post_login(email, password):
    password = encrypt_password(password)
    t = Trabajador.query.filter(Trabajador.email == email).one_or_none()
    if t:
        if t.password == password:
            return jwt.encode({"email": t.email, "rol": t.cargo, "exp": expire_date(app.config['EXPIRE_TOKEN_TIME'])}, app.config['SECRET_KEY'], algorithm="HS256")

    return None


def get_logout(current_trabajador):
    # DO TOKEN BLACKLIST
    current_trabajador.ultimo_acceso = datetime.now()
    db.session.commit()
    return None
