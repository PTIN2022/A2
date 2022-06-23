import controller.estacionesController as control
from flask import Blueprint, jsonify
from utils.utils import token_required

estaciones = Blueprint('estaciones', __name__)


@estaciones.route('/estaciones', methods=['GET'])
def get_estaciones():
    respuesta = control.get_all_estaciones()
    return jsonify(respuesta)


@estaciones.route('/estaciones/<id>', methods=["GET"])
@token_required
def get_estacion_by_id(current_usuario, id):
    if current_usuario:
        respuesta = control.get_estacion_by_id(id)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Station not found"}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@estaciones.route('/estaciones/coor/<lat>/<long>/<ratio>', methods=["GET"])
@token_required
def get_estacion_by_coor(current_usuario, lat, long, ratio):
    if current_usuario:
        respuesta = control.get_estacion_by_coor(lat, long, ratio)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Station not found"}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
