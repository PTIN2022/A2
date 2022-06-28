import controller.clienteController as control
from flask import Blueprint, jsonify, request
from utils.utils import token_required

clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes', methods=['GET'])
@token_required
def get_clientes(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        respuesta = control.get_all_clientes()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que hacer el error 401


@clientes.route('/clientes/bydni/<DNI>', methods=['GET'])
@token_required
def get_clientes_dni(current_trabajador, DNI):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
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
def get_clientes_id(current_trabajador, id):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
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
def post_cliente(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        nombre = request.form.to_dict()["nombre"]
        apellido = request.form.to_dict()["apellido"]
        email = request.form.to_dict()["email"]
        DNI = request.form.to_dict()["DNI"]
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
def deleted_cliente_dni(current_trabajador, DNI):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
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
def deleted_cliente_id(current_trabajador, id):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        deleted = control.delete_cliente_id(id)
        if deleted:
            return jsonify({"msg": "cliente deleted succesfully"}), 200
        else:
            return jsonify({"error": "cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@clientes.route('/clientes/bydni/<DNI>', methods=["PUT"])
@token_required
def modify_cliente_dni(current_trabajador, DNI):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        nombre = None
        apellido = None
        email = None
        dni_change = None
        foto = None
        telefono = None
        username = None
        password = None
        saldo = None

        if "name" in request.form.to_dict():
            nombre = request.form.to_dict()["name"]
        if "lastname" in request.form.to_dict():
            apellido = request.form.to_dict()["lastname"]
        if "email" in request.form.to_dict():
            email = request.form.to_dict()["email"]
        if "dni" in request.form.to_dict():
            dni_change = request.form.to_dict()["dni"]
        if "picture" in request.form.to_dict():
            foto = request.form.to_dict()["picture"]
        if "telf" in request.form.to_dict():
            telefono = request.form.to_dict()["telf"]
        if "username" in request.form.to_dict():
            username = request.form.to_dict()["username"]
        if "password" in request.form.to_dict():
            password = request.form.to_dict()["password"]
        if "saldo" in request.form.to_dict() and current_trabajador.cargo == "administrador":
            saldo = request.form.to_dict()["saldo"]
        respuesta = control.modify_cliente_dni(DNI, nombre, apellido, email, dni_change, foto, telefono, username, password, saldo)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@clientes.route('/clientes/<id>', methods=["PUT"])
@token_required
def modify_cliente_id(current_trabajador, id):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        nombre = None
        apellido = None
        email = None
        dni_change = None
        foto = None
        telefono = None
        username = None
        password = None
        saldo = None

        if "name" in request.form.to_dict():
            nombre = request.form.to_dict()["name"]
        if "lastname" in request.form.to_dict():
            apellido = request.form.to_dict()["lastname"]
        if "email" in request.form.to_dict():
            email = request.form.to_dict()["email"]
        if "dni" in request.form.to_dict():
            dni_change = request.form.to_dict()["dni"]
        if "picture" in request.form.to_dict():
            foto = request.form.to_dict()["picture"]
        if "telf" in request.form.to_dict():
            telefono = request.form.to_dict()["telf"]
        if "username" in request.form.to_dict():
            username = request.form.to_dict()["username"]
        if "password" in request.form.to_dict():
            password = request.form.to_dict()["password"]
        if "saldo" in request.form.to_dict() and current_trabajador.cargo == "administrador":
            saldo = request.form.to_dict()["saldo"]
        respuesta = control.modify_cliente_id(id, nombre, apellido, email, dni_change, foto, telefono, username, password, saldo)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "cliente not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
