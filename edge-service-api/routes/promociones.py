import controller.promocionesController as control
from flask import Blueprint, jsonify

promociones = Blueprint('promociones', __name__)

@promociones.route('/promociones/estaciones/<id_electrolinera>', methods=['GET'])
def get_all_promociones(id_electrolinera):
    respuesta = control.get_all_promociones(id_electrolinera)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promociones not found"}), 404


@promociones.route('/promociones/<id_promocion>', methods=["GET"])
def get_promocion_by_id(id_promocion):
    respuesta = control.get_promocion_by_id(id_promocion)
    print(respuesta)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promociones not found"}), 404

