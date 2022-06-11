from datetime import datetime
import controller.estadisticasController as control
from flask import Blueprint, jsonify
from utils import errors
from utils.utils import token_required
from models.model import Estacion

estadisticas = Blueprint('estadisticas', __name__)


@estadisticas.route('/estadisticas', methods=['GET'])
@token_required
def get_all_estadisticas(current_trabajador):
    if current_trabajador.cargo == "trabajador":
        return jsonify({"error": "User not authorized."}), 401
    if current_trabajador.cargo == "administrador":
        respuesta = control.get_all_estadisticas()
    elif current_trabajador.cargo == "encargado":
        data_inicio_d = datetime.strptime('2022-01-01', '%Y-%m-%d').date()
        data_final_d = datetime.strptime('2022-12-31', '%Y-%m-%d').date()
        respuesta = control.get_estadisticas_by_estacion(current_trabajador.id_estacion, data_inicio_d, data_final_d)
    return jsonify(respuesta)


@estadisticas.route('/estadisticas/<estacion>/<data_inicio>/<data_final>', methods=["GET"])
def get_estadisticas_by_estacion(current_trabajador, estacion, data_inicio, data_final):
    if current_trabajador.cargo == "encargado":
        if str(current_trabajador.id_estacion) != str(estacion):
            return jsonify({"error": "User not authorized."}), 401
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
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
    else:
        return jsonify({"error": "User not authorized."}), 401
