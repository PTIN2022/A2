from datetime import datetime
import controller.estadisticasController as control
from flask import Blueprint, jsonify
from utils import errors

estadisticas = Blueprint('estadisticas', __name__)


@estadisticas.route('/estadisticas', methods=['GET'])
def get_all_estadisticas():
    respuesta = control.get_all_estadisticas()
    return jsonify(respuesta)


@estadisticas.route('/estadisticas/<estacion>/<data_inicio>/<data_final>', methods=["GET"])
def get_estadisticas_by_estacion(estacion, data_inicio, data_final):
    data_inicio_d = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    data_final_d = datetime.strptime(data_final, '%Y-%m-%d').date()
    if data_inicio_d <= data_final_d:
        respuesta = control.get_estadisticas_by_estacion(estacion, data_inicio_d, data_final_d)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Estacion not found"}), 404
    else:
        return jsonify(errors.malformed_error()), 400
