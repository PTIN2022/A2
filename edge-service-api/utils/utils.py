
import hashlib
import jwt

from functools import wraps
from flask import jsonify, request
from flask import current_app as app
from models.model import Cliente



def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_usuario = Cliente.query.filter(Cliente.email == data['email']).one_or_none()
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'token is expired'})
        except:  # noqa E722
            return jsonify({'message': 'token is invalid'})
        return f(current_usuario, *args, **kwargs)
    return decorator


def encrypt_password(password):

    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        app.config['SALT'],  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )

    return key
