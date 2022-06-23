import controller.vehiculosController as control
from utils import errors
from flask import Blueprint, jsonify, request
from utils.utils import token_required

vehiculos = Blueprint('vehiculos', __name__)


@vehiculos.route('/vehiculos', methods=['GET'])
@token_required
# que vea los vehiculos solo relacionados con su token?
def get_all_vehiculos(current_usuario):
    if current_usuario:
        respuesta = control.get_all_vehiculos()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


# to do
@vehiculos.route('/vehiculos', methods=['POST'])
@token_required
# relacionar el vehiculo con el token iniciado
def post_vehiculos(current_usuario):
    if current_usuario:
        try:
            matricula = request.json["matricula"]
            modelo = request.json["modelo"]
            porcentaje_bat = request.json["porcentaje_bat"]
            respuesta = control.post_vehiculo(current_usuario, matricula, modelo, porcentaje_bat)
            if not respuesta:
                return ({"error": "Modelo not found. "}), 404

            return jsonify(respuesta)
        except ValueError:
            return jsonify(errors.malformed_error()), 400
        except KeyError:
            return jsonify(errors.malformed_error()), 400
    else:
        return jsonify({"error": "User not authorized."}), 401


@vehiculos.route('/vehiculos/<matricula>', methods=["GET"])
@token_required
# devolver el vehiculo con matricula solo si esta relacionado con su token
def get_vehiculos_by_matricula(current_usuario, matricula):
    if current_usuario:
        respuesta = control.get_vehiculo_by_matricula(current_usuario, matricula)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Vehiculo not found or Vehicle is not yours."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@vehiculos.route('/vehiculos/cliente', methods=["GET"])
@token_required
def get_vehiculo_by_idcliente(current_usuario):
    if current_usuario:
        respuesta = control.get_vehiculo_by_idcliente(current_usuario)
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "User not authorized."}), 401


@vehiculos.route('/vehiculos/<matricula>', methods=["PUT"])
@token_required
# solo puede modificar sus vehiculos? si es admin?
def modify_matricula(current_usuario, matricula):
    if current_usuario:
        porcentaje_bat = None

        if "porcentaje_bat" in request.json:
            porcentaje_bat = request.json["porcentaje_bat"]

        respuesta = control.modify_vehiculo(current_usuario, matricula, porcentaje_bat)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Vehiculo not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@vehiculos.route('/vehiculos/<matricula>', methods=["DELETE"])
@token_required
# solo puede borrar si el token es el relacionado con el coche? admins tambn?
def deleted_vehiculo_matr(current_usuario, matricula):
    if current_usuario:
        deleted = control.delete_vehiculo_matr(matricula)
        if deleted:
            return jsonify({"msg": "Vehiculo deleted correctly."}), 200
        else:
            return jsonify({"error": "Vehiculo not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
