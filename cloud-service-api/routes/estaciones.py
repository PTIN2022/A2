import controller.estacionesController as control
from flask import Blueprint, jsonify


estaciones = Blueprint('estaciones', __name__)


@estaciones.route('/estaciones', methods=['GET'])
def get_estaciones():
    respuesta = control.get_all_estaciones()
    return jsonify(respuesta)


@estaciones.route('/estaciones/<id>', methods=["GET"])
def get_estacion_by_id(id):
    respuesta = control.get_estacion_by_id(id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Estacion not found"}), 404


@estaciones.route('/estaciones/coor/<lat>/<long>', methods=["GET"])
def get_estacion_by_coor(lat, long):
    respuesta = control.get_estacion_by_coor(lat, long)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Station not found"}), 404
