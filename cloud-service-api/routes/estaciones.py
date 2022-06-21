import controller.estacionesController as control
from flask import Blueprint, jsonify, request
from utils.utils import token_required


estaciones = Blueprint('estaciones', __name__)


@estaciones.route('/estaciones', methods=['GET'])
@token_required
def get_estaciones(current_trabajador):
    if current_trabajador.cargo == "trabajador" or current_trabajador.cargo == "encargado":
        respuesta = control.get_estacion_by_id(int(current_trabajador.id_estacion))
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Estacion not found"}), 404
    elif current_trabajador.cargo == "administrador":
        respuesta = control.get_all_estaciones()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@estaciones.route('/estaciones/<id>', methods=["GET"])
@token_required
def get_estacion_by_id(current_trabajador, id):
    if current_trabajador.cargo == "encargado" or current_trabajador.cargo == "administrador":
        respuesta = control.get_estacion_by_id(int(id))
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Estacion not found"}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401

@estaciones.route('/estaciones/<id>', methods=["PUT"])
@token_required
def put_estacion_by_id(current_trabajador, id):
    if current_trabajador.cargo == "encargado" or current_trabajador.cargo == "administrador":
        latitud = None
        longitud = None
        capacidad = None
        direccion = None
        estado = None
        telefono = None
        potencia_contratada = None
        potencia_usada = None
        potencia_actual = None
        zona = None
        if "latitud" in request.json:
            latitud = request.json["latitud"]
        if "longitud" in request.json:
            longitud = request.json["longitud"]
        if "capacidad" in request.json:
            capacidad = request.json["capacidad"]
        if "direccion" in request.json:
            direccion = request.json["direccion"]
        if "estado" in request.json:
            estado = request.json["estado"]
        if "telefono" in request.json:
            telefono = request.json["telefono"]
        if "potencia_contratada" in request.json:
            potencia_contratada = request.json["potencia_contratada"]
        if "potencia_usada" in request.json:
            potencia_usada = request.json["potencia_usada"]
        if "potencia_actual" in request.json:
            potencia_actual = request.json["potencia_actual"]
        if "zona" in request.json:
            zona = request.json["zona"]
        respuesta= control.put_estacion_by_id(int(id), latitud, longitud, capacidad, direccion, estado, telefono, potencia_contratada, potencia_usada, potencia_actual, zona)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Estacion not found"}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401

@estaciones.route('/estaciones/<id>/<id_plaza>', methods=["DELETE"])
@token_required
def delete_plaza(current_trabajador, id, id_plaza):
    if current_trabajador.cargo == "encargado":
        if str(current_trabajador.id_estacion) != str(id):
            return jsonify({"error": "User not authorized."}), 401
    if current_trabajador.cargo == "encargado" or current_trabajador.cargo == "administrador":
        respuesta = control.delete_plaza(id, id_plaza)
        if respuesta:
            return jsonify({"msg": "Data deleted correctly."}), 200
        else:
            return jsonify({"error": "Plaza or Estacion not found"}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
