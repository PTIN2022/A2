import controller.clienteController as control
from flask import Blueprint, jsonify, request
from utils import errors
from utils.utils import token_required
from models.model import Cliente
clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes', methods=['GET'])
@token_required
def get_clientes(current_usuario):
    if current_usuario:
        respuesta = control.get_all_clientes()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que hacer el error 401


@clientes.route('/clientes/bydni/<DNI>', methods=['GET'])
@token_required
def get_clientes_dni(current_usuario, DNI):
    if current_usuario:
        respuesta = control.get_cliente_dni(DNI)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que meter el error 401


@clientes.route('/clientes/<id>', methods=['GET'])
@token_required
def get_clientes_id(current_usuario, id):
    if current_usuario:
        respuesta = control.get_cliente_id(id)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que meter el error 401


@clientes.route('/clientes', methods=['POST'])
def post_cliente():
    try:
        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        email = request.json["email"]
        DNI = request.json["DNI"]
        client_exist = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
        if client_exist:
            return jsonify({"error": "Cliente already exist."}), 400
        foto = request.json["foto"]
        telefono = request.json["telefono"]
        username = request.json["username"]
        password = request.json["password"]
        c = control.post_cliente(nombre, apellido, email, DNI, foto, telefono, username, password)
        return jsonify(c)
    except ValueError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400
    except KeyError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400


@clientes.route('/clientes/bydni/<DNI>', methods=["DELETE"])
@token_required
def deleted_cliente_dni(current_usuario, DNI):
    if current_usuario:
        deleted = control.delete_cliente_dni(DNI)
        if deleted:
            return jsonify({"msg": "cliente deleted succesfully"}), 200
        else:
            return jsonify({"error": "cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que hacer error 401


@clientes.route('/clientes/<id>', methods=["DELETE"])
@token_required
def deleted_cliente_id(current_usuario, id):
    if current_usuario:
        deleted = control.delete_cliente_id(id)
        if deleted:
            return jsonify({"msg": "cliente deleted succesfully"}), 200
        else:
            return jsonify({"error": "cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que hacer error 401


@clientes.route('/clientes', methods=["PUT"])
@token_required
def modify_cliente(current_usuario):
    if current_usuario:
        nombre = None
        apellido = None
        email = None
        foto = None
        telefono = None
        username = None
        password = None
        saldo = None
        if request.json["nombre"]:
            nombre = request.json["nombre"]
        if request.json["apellido"]:
            apellido = request.json["apellido"]
        if request.json["email"]:
            email = request.json["email"]
        if request.json["foto"]:
            foto = request.json["foto"]
        if request.json["telefono"]:
            telefono = request.json["telefono"]
        if request.json["username"]:
            username = request.json["username"]
        if request.json["password"]:
            password = request.json["password"]
        if request.json["saldo"]:
            saldo = request.json["saldo"]
        respuesta = control.modify_cliente(current_usuario.dni, nombre, apellido, email, foto, telefono, username, password, saldo)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
