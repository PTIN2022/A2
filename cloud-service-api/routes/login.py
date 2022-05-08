import controller.loginController as control

from flask import Blueprint, jsonify, request
from utils import utils, errors
import jwt
from datetime import datetime, timedelta

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)


@login.route('/login', methods=['POST'])
def post_login():
    email = request.form.to_dict()["email"]
    password = request.form.to_dict()["password"]

    exists = control.post_login(email, password)

    if exists:
        encoded_jwt = jwt.encode({"email": exists['email'], "exp": expire_date(2)}, "secret", algorithm="HS256")
        return jsonify({'token': encoded_jwt}), 200
    else:
        return jsonify({'error' : 'Invalid credendtials'}), 400


def expire_date(days):
    now = datetime.now()
    new_date = now + timedelta(days)
    return new_date


@logout.route('/logout', methods=['GET'])
def get_logout():
    return jsonify({'error' : 'Invalid credendtials'}), 200
