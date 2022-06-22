import controller.clienteController as control
from flask import Blueprint, jsonify, request
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
@token_required
def post_cliente(current_usuario):
    if current_usuario:

        nombre = request.form.to_dict()["nombre"]
        apellido = request.form.to_dict()["apellido"]
        email = request.form.to_dict()["email"]
        DNI = request.form.to_dict()["DNI"]
        client_exist = Cliente.query.filter(Cliente.dni == DNI).one_or_none()
        if client_exist:
            return jsonify({"error": "Cliente already exist."}), 400
        foto = request.form.to_dict()["foto"]
        telefono = request.form.to_dict()["telefono"]
        username = request.form.to_dict()["username"]
        password = request.form.to_dict()["password"]
        c = control.post_cliente(nombre, apellido, email, DNI, foto, telefono, username, password)
        return jsonify(c)
    else:
        return jsonify({"error": "User not authorized."}), 401


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
