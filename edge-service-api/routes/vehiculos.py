import controller.vehiculosController as control
from utils import errors
from datetime import datetime
from flask import Blueprint, jsonify, request
# from utils.utils import token_required

vehiculos = Blueprint('vehiculos', __name__)


@vehiculos.route('/vehiculos', methods=['GET'])
# @token_required
# que vea los vehiculos solo relacionados con su token?
def get_all_vehiculos():
    respuesta = control.get_all_vehiculos()
    return jsonify(respuesta)


# to do
@vehiculos.route('/vehiculos', methods=['POST'])
# @token_required
# relacionar el vehiculo con el token iniciado
def post_vehiculos():
    try:
        matricula = request.json["matricula"]
        modelo = request.json["modelo"]
        porcentaje_bat = request.json["porcentaje_bat"]
        respuesta = control.post_vehiculo(matricula, modelo, porcentaje_bat)
        if not respuesta:
            return ({"error": "Modelo not found. "}), 404

        return jsonify(respuesta)
    except ValueError:
        return jsonify(errors.malformed_error()), 400
    except KeyError:
        return jsonify(errors.malformed_error()), 400


@vehiculos.route('/vehiculos/<matricula>', methods=["GET"])
# @token_required
# devolver el vehiculo con matricula solo si esta relacionado con su token
def get_vehiculos_by_matricula(matricula):
    respuesta = control.get_vehiculo_by_matricula(matricula)
    if respuesta != None:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Vehiculo not found."}), 404


@vehiculos.route('/vehiculos/cliente/<id_cliente>', methods=["GET"])
# @token_required
# se elimina?!!!!!!!!!!!!!!!!!!!!
def get_vehiculo_by_idcliente(id_cliente):
    respuesta = control.get_vehiculo_by_idcliente(id_cliente)
    return jsonify(respuesta), 200


@vehiculos.route('/vehiculos/<matricula>', methods=["PUT"])
# @token_required
# solo puede modificar sus vehiculos? si es admin?
def modify_matricula(matricula):
    porcentaje_bat = None

    if "porcentaje_bat" in request.json:
        porcentaje_bat = request.json["porcentaje_bat"]
        print ("bbbbb",porcentaje_bat)

    respuesta = control.modify_vehiculo(matricula, porcentaje_bat)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Vehiculo not found."}), 404


@vehiculos.route('/vehiculos/<matricula>', methods=["DELETE"])
# @token_required
# solo puede borrar si el token es el relacionado con el coche? admins tambn?
def deleted_vehiculo_matr(matricula):
    deleted = control.delete_vehiculo_matr(matricula)
    if deleted:
        return jsonify({"msg": "Vehiculo deleted correctly."}), 200
    else:
        return jsonify({"error": "Vehiculo not found."}), 404
