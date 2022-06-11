import controller.trabajadorController as control
from flask import Blueprint, jsonify, request
from datetime import datetime

trabajador = Blueprint('trabajadores', __name__)


@trabajador.route('/trabajador', methods=['GET'])
def get_trabajadores():
    respuesta = control.get_all_trabajadores()
    return jsonify(respuesta)
# habra que hacer el error 401


@trabajador.route('/trabajador/<dni>', methods=['GET'])
def get_trabajadores_dni(dni):
    respuesta = control.get_trabajador_dni(dni)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Trabajador not found."}), 404
# habra que meter el error 401


@trabajador.route('/trabajador', methods=['POST'])
def post_trabajador():
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
    if t:
        return jsonify(t)
    else:
        return jsonify({"error": "No se pudo encontrar esta estacion"})


@trabajador.route('/trabajador/<dni>', methods=["PUT"])
def modify_trabajador(dni):
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

    if "nombre," in request.form.to_dict():
        nombre = request.form.to_dict()["nombre,"]
    if "apellido" in request.form.to_dict():
        apellido = request.form.to_dict()["apellido"]
    if "email" in request.form.to_dict():
        email = request.form.to_dict()["email"]
    if "dni" in request.form.to_dict():
        dni_change = request.form.to_dict()["dni"]
    if "picture" in request.form.to_dict():
        foto = "https://this-person-does-not-exist.com/img/avatar-754c5f55152107173073b232e864e6b.jpg"
    if "telefono" in request.form.to_dict():
        telefono = request.form.to_dict()["telefono"]
    if "username" in request.form.to_dict():
        username = request.form.to_dict()["username"]
    if "password" in request.form.to_dict():
        password = request.form.to_dict()["password"]
    if "cargo" in request.form.to_dict():
        cargo = request.form.to_dict()["cargo"]
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
# habra que hacer error 400


@trabajador.route('/trabajador/<dni>', methods=["DELETE"])
def deleted_trabajador(dni):
    deleted = control.delete_trabajador(dni)
    if deleted:
        return jsonify({"msg": "Trabajador deleted succesfully"}), 200
    else:
        return jsonify({"error": "Trabajador not found."}), 404
# habra que hacer error 401
