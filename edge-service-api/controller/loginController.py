import jwt
from utils.db import db
from flask import current_app as app
from datetime import datetime, timedelta
from utils.utils import encrypt_password
from models.usuario import Usuario, UsuarioSchema


def expire_date(minutes):
    now = datetime.utcnow()
    new_date = now + timedelta(minutes=minutes)
    return new_date


def post_login(username, password):
    password = encrypt_password(password)
    t = Usuario.query.filter(Usuario.username == username).one_or_none()
    if t:
        if t.password == password:
            db.session.commit()
            return jwt.encode({"username": t.username, "exp": expire_date(app.config['EXPIRE_TOKEN_TIME'])}, app.config['SECRET_KEY'], algorithm="HS256")

    return None


def get_logout():
    return None
