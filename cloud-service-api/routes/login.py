import controller.loginController as control
from utils.utils import token_required

from flask import Blueprint, jsonify, request

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
        return jsonify({'error': 'Invalid credendtials'}), 400


@logout.route('/logout', methods=['GET'])
@token_required
def get_logout(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        control.get_logout(current_trabajador)
        return jsonify({'Succes': 'Logout done'}), 200
    else:
        return jsonify({'error': 'User not authorized'}), 400
