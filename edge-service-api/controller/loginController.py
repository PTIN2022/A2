import jwt
from flask import current_app as app
from datetime import datetime, timedelta
from utils.utils import encrypt_password
from models.model import Cliente, ClienteSchema


def expire_date(minutes):
    now = datetime.utcnow()
    new_date = now + timedelta(minutes=minutes)
    return new_date


def post_login(username, password):
    password = encrypt_password(password)
    c = Cliente.query.filter(Cliente.email == username).one_or_none()
    if c:
        if c.password == password:
            return jwt.encode({"email": c.email, "DNI": c.dni, "exp": expire_date(app.config['EXPIRE_TOKEN_TIME'])}, app.config['SECRET_KEY'], algorithm="HS256"), ClienteSchema().dump(c)

    return None


def get_logout():
    return None
