import controller.loginController as control
from utils.utils import token_required
from models.model import TrabajadorSchema
from flask import Blueprint, jsonify, request

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)


@login.route('/login', methods=['POST'])
def post_login():
    email = request.form.to_dict()["email"]
    password = request.form.to_dict()["password"]
    trabajador = control.post_login(email, password)
    print(type(trabajador))
    print(trabajador)

    if trabajador:
        return jsonify(trabajador), 200
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


@logout.route('/token', methods=['GET'])
@token_required
def get_info(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        respuesta = TrabajadorSchema().dump(current_trabajador)
        return jsonify(respuesta), 200
    else:
        return jsonify({'error': 'User not authorized'}), 400