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


@estaciones.route('/estaciones/<id>/<id_plaza>', methods=["DELETE"])
def delete_plaza(id, id_plaza):
    respuesta = control.delete_plaza(id, id_plaza)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Plaza or Estacion not found"}), 404
