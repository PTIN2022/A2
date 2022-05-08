import jwt
from models.trabajador import Trabajador
from functools import wraps
from flask import jsonify, request


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
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_trabajador, *args, **kwargs)
   return decorator
