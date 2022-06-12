import controller.estacionesController as control
from flask import Blueprint, jsonify
from utils.utils import token_required


estaciones = Blueprint('estaciones', __name__)


@estaciones.route('/estaciones', methods=['GET'])
@token_required
def get_estaciones(current_trabajador):
    if current_trabajador.cargo == "trabajador":
        return jsonify({"error": "User not authorized."}), 401
    elif current_trabajador.cargo == "administrador":
        respuesta = control.get_all_estaciones()
        return jsonify(respuesta)
    elif current_trabajador.cargo == "encargado":
        respuesta = control.get_estacion_by_id(int(current_trabajador.id_estacion))
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Estacion not found"}), 404


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
