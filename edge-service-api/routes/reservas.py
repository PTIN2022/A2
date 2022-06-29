import controller.reservasController as control
from utils import errors
from datetime import datetime
from flask import Blueprint, jsonify, request
from utils.utils import token_required

reservas = Blueprint('reservas', __name__)


@reservas.route('/reservas', methods=['GET'])
@token_required
def get_reservas(current_usuario):
    if current_usuario:
        respuesta = control.get_all_reservas()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas', methods=['POST'])
@token_required
def post_reservas(current_usuario):
    if current_usuario:
        try:
            print(request.json)
            estacion = request.json["id_estacion"]
            fecha_inicio = request.json["fecha_inicio"]  # Dia y hora
            fecha_final = request.json["fecha_final"]
            fecha_final_str = datetime.strptime(fecha_final, '%d-%m-%Y %H:%M')
            fecha_inicio_str = datetime.strptime(fecha_inicio, '%d-%m-%Y %H:%M')
            matricula = request.json["id_vehiculo"]
            DNI = current_usuario.dni
            tarifa = request.json["tarifa"]
            asistida = request.json["asistida"]
            porcentaje_carga = request.json["porcentaje_carga"]
            precio_carga_completa = request.json["precio_carga_completo"]
            precio_carga_actual = request.json["precio_carga_actual"]
            estado_pago = request.json["estado_pago"]
            # TODO: comprobar fecha final es mayor fecha inicial
            reserva = control.post_reserva(estacion, matricula, tarifa, asistida, porcentaje_carga, precio_carga_completa, precio_carga_actual, estado_pago, fecha_inicio_str, fecha_final_str, DNI)
            if type(reserva) == dict:
                print(reserva)
                return jsonify(reserva), 406
            else:
                respuesta = control.get_reservas_id(reserva)
            return jsonify(respuesta)

        except ValueError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
        except KeyError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/<id>', methods=["GET"])
@token_required
def get_reserva_by_id(current_usuario, id):
    if current_usuario:
        respuesta = control.get_reservas_id(id)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Reserva not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/estacion/<id_estacion>', methods=["GET"])
@token_required
def get_reserva_by_estacio(current_usuario, id_estacion):
    if current_usuario:
        respuesta = control.get_reservas_estacion(id_estacion)
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/bymatricula/<matricula>', methods=["GET"])
@token_required
def get_reserva_by_matricula(current_usuario, matricula):
    if current_usuario:
        respuesta = control.get_reservas_matricula(matricula)
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/bydni/<dni>', methods=["GET"])
@token_required
def get_reserva_by_dni(current_usuario, dni):
    if current_usuario:
        respuesta = control.get_reservas_dni(dni)
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/<id>', methods=["DELETE"])
@token_required
def deleted_reservas(current_usuario, id):
    if current_usuario:
        deleted = control.remove_reserva(id)
        if deleted:
            return jsonify({"msg": "Data deleted correctly."}), 200
        else:
            return jsonify({"error": "Reserva not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
