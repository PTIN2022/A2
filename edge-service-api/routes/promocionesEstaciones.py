import controller.promocionesEstacionesController as controlPromocionEstacion
from flask import Blueprint, jsonify

promocionesEstaciones = Blueprint('promocionesEstaciones', __name__)


@promocionesEstaciones.route('/promocionesEstaciones', methods=['GET'])
def get_promociones_estaciones():
    respuesta = controlPromocionEstacion.get_all_promociones_estaciones()
    return jsonify(respuesta)


@promocionesEstaciones.route('/promocionesEstaciones/<id_promo>', methods=["GET"])
def get_id_promcion_estaciones(id_promo):
    respuesta = controlPromocionEstacion.get_id_promociones_estaciones(id_promo)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion con estacion not found"}), 404


@promocionesEstaciones.route('/promocionesEstaciones/<id_promo>/<id_estacion>', methods=["POST"])
def post_promcion_id_estaciones(id_promo, id_estacion):
    respuesta = controlPromocionEstacion.post_promociones_estaciones(id_promo, id_estacion)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion con estacion not found"}), 404


