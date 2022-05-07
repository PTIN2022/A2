import controller.loginController as control

from flask import Blueprint, jsonify, request
from utils import utils, errors
import jwt
from datetime import datetime

login = Blueprint('login', __name__)


@login.route('/login', methods=['POST'])
def post_login():
    email = request.form.to_dict()["email"]
    password = request.form.to_dict()["password"]

    exists = control.post_login(email, password)

    if exists:
        encoded_jwt = jwt.encode({"email": exists['email'], "password": exists['password']}, "secret", algorithm="HS256")
        return jsonify({'token': encoded_jwt}), 200
    else:
        return jsonify(errors.malformed_error()), 400
