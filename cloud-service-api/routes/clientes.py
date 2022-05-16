import controller.clienteController as control
from flask import Blueprint, jsonify, request

clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes', methods=['GET'])
def get_clientes():
    respuesta = control.get_all_clientes()
    return jsonify(respuesta)
# habra que hacer el error 401


@clientes.route('/clientes/bydni/<DNI>', methods=['GET'])
def get_clientes_dni(DNI):
    respuesta = control.get_cliente_dni(DNI)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "cliente not found."}), 404
# habra que meter el error 401

@clientes.route('/clientes/<id>', methods=['GET'])
def get_clientes_id(id):
    respuesta = control.get_cliente_id(id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "cliente not found."}), 404
# habra que meter el error 401

@clientes.route('/clientes', methods=['POST'])
def post_cliente():
    nombre = request.form.to_dict()["nombre"]
    apellido = request.form.to_dict()["apellido"]
    email = request.form.to_dict()["email"]
    DNI = request.form.to_dict()["DNI"]
    foto = request.form.to_dict()["foto"]
    telefono = request.form.to_dict()["telefono"]
    username = request.form.to_dict()["username"]
    password = "123"
    c = control.post_cliente(nombre, apellido, email, DNI, foto, telefono, username, password)
    return jsonify(c)


@clientes.route('/clientes/bydni/<DNI>', methods=["DELETE"])
def deleted_cliente_dni(DNI):
    deleted = control.delete_cliente_dni(DNI)
    if deleted:
        return jsonify({"msg": "cliente deleted succesfully"}), 200
    else:
        return jsonify({"error": "cliente not found."}), 404
# habra que hacer error 401

@clientes.route('/clientes/<id>', methods=["DELETE"])
def deleted_cliente_id(id):
    deleted = control.delete_cliente_id(id)
    if deleted:
        return jsonify({"msg": "cliente deleted succesfully"}), 200
    else:
        return jsonify({"error": "cliente not found."}), 404
# habra que hacer error 401