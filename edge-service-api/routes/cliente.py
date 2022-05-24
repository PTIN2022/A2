import controller.ClienteController as control
from flask import Blueprint, jsonify, request

clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes', methods=['GET'])
def get_clientes():
    respuesta = control.get_all_clientes()
    return jsonify(respuesta), 200
    # habra que hacer control de quien hacer el get all


@clientes.route('/clientes/profile/<DNI>', methods=['GET'])
def get_clientes_dni(DNI):
    respuesta = control.get_cliente_dni(DNI)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "User not found."}), 404
# habra que meter el error 401


@clientes.route('/clientes/profile/<DNI>/reservas', methods=['GET'])
def get_clientes_reservas(DNI):
    respuesta = control.get_cliente_reservas(DNI)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Reserva not found for this user."}), 404


@clientes.route('/clientes', methods=['POST'])
def post_cliente():
    nombre = request.json["nombre"]
    apellido = request.json["apellido"]
    email = request.json["email"]
    DNI = request.json["DNI"]
    foto = request.json["foto"]
    telefono = request.json["telefono"]
    username = request.json["username"]
    password = request.json["password"]
    c = control.post_cliente(nombre, apellido, email, DNI, foto, telefono, username, password)
    return jsonify(c)


@clientes.route('/clientes/profile/<DNI>', methods=["PUT"])
def modify_cliente_dni(DNI):
    nombre = None
    apellido = None
    email = None
    foto = None
    password = None
    username = None
    telefono = None

    try:
        nombre = request.json["nombre"]
        apellido = request.json["apellido"]
        email = request.json["email"]
        telefono = request.json["telefono"]
        foto = "https://editor.swagger.io/"
    except:
    	return jsonify({"error": "Malformed request syntax."}), 400
    respuesta = control.modify_cliente(nombre, apellido, email, DNI, foto, telefono)
    
    if respuesta:
        return jsonify({"msg": "User modified succesfully"}), 200
    else:
        return jsonify({"error": "User not found."}), 404
# habra que hacer error 401


@clientes.route('/clientes/change_password/<DNI>', methods=["PUT"])
def modify_password(DNI):
    try:
        last_password = request.json["actual_password"]
        new_password = request.json["new_password"]
    except:
    	return jsonify({"error": "Malformed request syntax."}), 400
    respuesta = control.modify_password(DNI, last_password, new_password)
    if respuesta:
        return jsonify({"msg": "Password changed succesfully."}), 200
    else:
        return jsonify({"error": "User not found."}), 404


@clientes.route('/clientes/profile/<DNI>', methods=["DELETE"])
def deleted_cliente_dni(DNI):
    deleted = control.delete_cliente_dni(DNI)
    if deleted:
        return jsonify({"msg": "User deleted succesfully"}), 200
    else:
        return jsonify({"error": "User not found."}), 404
# habra que hacer error 401
