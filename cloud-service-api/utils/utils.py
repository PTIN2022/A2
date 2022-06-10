import hashlib
import jwt
from functools import wraps
from flask import jsonify, request
from flask import current_app as app
from models.model import Trabajador

# https://stackoverflow.com/questions/42248342/yes-no-prompt-in-python3-using-strtobool
def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    else:
        raise ValueError("invalid truth value %r" % (val,))



# https://www.bacancytechnology.com/blog/flask-jwt-authentication
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
            current_trabajador = Trabajador.query.filter(Trabajador.email == data['email']).one_or_none()
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'token is expired'})
        except:  # noqa: E722
            # TODO: cuidado aqui va cualquier excepcion
            return jsonify({'message': 'token is invalid'})

        return f(current_trabajador, *args, **kwargs)
    return decorator


def encrypt_password(password):
    key = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        app.config['SALT'],  # Provide the salt
        100000  # It is recommended to use at least 100,000 iterations of SHA-256
    )
    return key