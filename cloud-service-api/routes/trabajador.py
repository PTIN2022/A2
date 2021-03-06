import controller.trabajadorController as control
from flask import Blueprint, jsonify, request
from datetime import datetime
from utils.utils import token_required

trabajador = Blueprint('trabajadores', __name__)


@trabajador.route('/trabajador', methods=['GET'])
@token_required
def get_trabajadores(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        respuesta = control.get_all_trabajadores()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que hacer el error 401


@trabajador.route('/trabajador/<dni>', methods=['GET'])
@token_required
def get_trabajadores_dni(current_trabajador, dni):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        respuesta = control.get_trabajador_dni(dni)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Trabajador not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que meter el error 401


@trabajador.route('/trabajador', methods=['POST'])
@token_required
def post_trabajador(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        nombre = request.form.to_dict()["nombre"]
        apellido = request.form.to_dict()["apellido"]
        email = request.form.to_dict()["email"]
        dni = request.form.to_dict()["dni"]
        foto = "https://this-person-does-not-exist.com/img/avatar-754c5f55152107173073b232e864e6b.jpg"
        telefono = request.form.to_dict()["telefono"]
        username = request.form.to_dict()["username"]
        password = request.form.to_dict()["password"]
        cargo = request.form.to_dict()["cargo"]
        estado = request.form.to_dict()["estado"]
        question = request.form.to_dict()["question"]
        id_estacion = request.form.to_dict()["id_estacion"]
        last_access = datetime.fromtimestamp(0)

        t = control.post_trabajador(nombre, apellido, email, dni, foto, telefono, username, password, cargo, estado, last_access, question, id_estacion)
        if "error" in t:
            return jsonify(t), 404

        return jsonify(t)
    else:
        return jsonify({"error": "User not authorized."}), 401


@trabajador.route('/trabajador/<dni>', methods=["PUT"])
@token_required
def modify_trabajador(current_trabajador, dni):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":

        nombre = None
        apellido = None
        email = None
        dni_change = None
        foto = None
        telefono = None
        username = None
        password = None
        cargo = None
        estado = None
        question = None
        id_estacion = None

        if "name" in request.form.to_dict():
            nombre = request.form.to_dict()["name"]
        if "lastname" in request.form.to_dict():
            apellido = request.form.to_dict()["lastname"]
        if "email" in request.form.to_dict():
            email = request.form.to_dict()["email"]
        if "dni" in request.form.to_dict():
            dni_change = request.form.to_dict()["dni"]
        if "profileImage" in request.form.to_dict():
            foto = "https://this-person-does-not-exist.com/img/avatar-754c5f55152107173073b232e864e6b.jpg"
        if "telf" in request.form.to_dict():
            telefono = request.form.to_dict()["telf"]
        if "username" in request.form.to_dict():
            username = request.form.to_dict()["username"]
        if "password" in request.form.to_dict():
            password = request.form.to_dict()["password"]
        if "rol" in request.form.to_dict():
            if current_trabajador.cargo == "administrador":
                cargo = request.form.to_dict()["rol"]
            else:
                return jsonify({"error": "User not authorized."}), 401
        if "estado" in request.form.to_dict():
            estado = request.form.to_dict()["estado"]
        if "question" in request.form.to_dict():
            question = request.form.to_dict()["question"]
        if "id_estacion" in request.form.to_dict():
            id_estacion = request.form.to_dict()["id_estacion"]

        respuesta = control.modify_trabajador(dni, nombre, apellido, email, dni_change, foto, telefono, username, password, cargo, estado, question, id_estacion)

        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Trabajador not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que hacer error 400


@trabajador.route('/trabajador/<dni>', methods=["DELETE"])
@token_required
def deleted_trabajador(current_trabajador, dni):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        deleted = control.delete_trabajador(dni)
        if deleted:
            return jsonify({"msg": "Trabajador deleted succesfully"}), 200
        else:
            return jsonify({"error": "Trabajador not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
# habra que hacer error 401
