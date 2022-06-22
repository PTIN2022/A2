import controller.modelosController as control
from utils import errors
from datetime import datetime
from flask import Blueprint, jsonify, request

modelos = Blueprint('modelos', __name__)


@modelos.route('/modelos', methods=['GET'])
def get_all_modelos():
    respuesta = control.get_all_modelos()
    return jsonify(respuesta)


# to do
@modelos.route('/modelos', methods=['POST'])
def post_modelos():
    try:
        modelo = request.json["modelo"]
        marca = request.json["marca"]
        potencia_carga = request.json["potencia_carga"]
        capacidad = request.json["capacidad"]

        respuesta = control.post_modelo(modelo, marca, potencia_carga, capacidad)
        return jsonify(respuesta)
    except ValueError:
        return jsonify(errors.malformed_error()), 400
    except KeyError:
        return jsonify(errors.malformed_error()), 400
