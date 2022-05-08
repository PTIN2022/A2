import controller.loginController as control

from flask import Blueprint, jsonify, request
from utils import utils, errors

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)


@login.route('/login', methods=['POST'])
def post_login():
    email = request.form.to_dict()["email"]
    password = request.form.to_dict()["password"]

    encoded_jwt = control.post_login(email, password)
    
    if encoded_jwt:
        return jsonify({'token': encoded_jwt}), 200
    else:
        return jsonify({'error' : 'Invalid credendtials'}), 400


@logout.route('/logout', methods=['GET'])
def get_logout():
    return jsonify({'error' : 'Invalid credendtials'}), 200
