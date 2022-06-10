import controller.reservasController as control
from models.trabajador import Trabajador
from utils import errors
from datetime import datetime
from flask import Blueprint, jsonify, request
from utils.utils import token_required

reservas = Blueprint('reservas', __name__)

@reservas.route('/reservas', methods=['GET'])
@token_required
def get_reservas(current_trabajador):
    if current_trabajador.rol == "admin":
        respuesta = control.get_all_reservas()
        return jsonify(respuesta)
    elif current_trabajador.rol == "responsable" or current_trabajador.rol == "tecnic":
        respuesta = control.get_reservas_estacion(current_trabajador.id_estacion)
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas', methods=['POST'])
@token_required
def post_reservas(current_trabajador):
    if current_trabajador.rol == "admin" or current_trabajador.rol == "responsable" or current_trabajador.rol == "tecnic":
        estacion = request.json["id_estacion"]
        if ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "responsable" ) or ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "tecnic" ):
            return jsonify({"error": "User not authorized."}), 401
        try:
            fecha_inicio = request.json["fecha_inicio"]  # Dia y hora
            fecha_final = request.json["fecha_final"]
            fecha_final_str = datetime.strptime(fecha_final, '%d-%m-%Y %H:%M')
            fecha_inicio_str = datetime.strptime(fecha_inicio, '%d-%m-%Y %H:%M')
            matricula = request.json["id_vehiculo"]
            DNI = request.json["id_cliente"]

            # TODO: comprobar fecha final es mayor fecha inicial
            id = control.post_reserva(estacion, matricula, fecha_inicio_str, fecha_final_str, DNI)
            respuesta, estacion = control.get_reservas_id(id)
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
def get_reserva_by_id(current_trabajador, id):
    if current_trabajador.rol == "admin" or current_trabajador.rol == "responsable" or current_trabajador.rol == "tecnic":
        respuesta, estacion = control.get_reservas_id(id)
        if ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "responsable" ) or ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "tecnic" ):
            return jsonify({"error": "User not authorized."}), 401
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Reserva not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/estacion/<id_estacion>', methods=["GET"])
@token_required
def get_reserva_by_estacio(current_trabajador, id_estacion):
    if current_trabajador.rol == "admin" or current_trabajador.rol == "responsable" or current_trabajador.rol == "tecnic":
        if ( id_estacion != current_trabajador.id_estacion and current_trabajador.rol == "responsable" ) or ( id_estacion != current_trabajador.id_estacion and current_trabajador.rol == "tecnic" ):
            return jsonify({"error": "User not authorized."}), 401
        respuesta = control.get_reservas_estacion(id_estacion)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Station not found."}), 40
    else:
        return jsonify({"error": "User not authorized."}), 401

@reservas.route('/reservas/bymatricula/<matricula>', methods=["GET"])
@token_required
def get_reserva_by_matricula(current_trabajador, matricula):
    if current_trabajador.rol == "admin" or current_trabajador.rol == "responsable" or current_trabajador.rol == "tecnic":
        respuesta, estacion = control.get_reservas_matricula(matricula)
        if ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "responsable" ) or ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "tecnic" ):
            return jsonify({"error": "User not authorized."}), 401
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Reserva not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/bydni/<dni>', methods=["GET"])
@token_required
def get_reserva_by_dni(current_trabajador, dni):
    if current_trabajador.rol == "admin" or current_trabajador.rol == "responsable" or current_trabajador.rol == "tecnic":
        respuesta, estacion = control.get_reservas_dni(dni)
        if ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "responsable" ) or ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "tecnic" ):
            return jsonify({"error": "User not authorized."}), 401
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Reserva not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@reservas.route('/reservas/<id>', methods=["DELETE"])
@token_required
def deleted_reservas(current_trabajador, id):
    if current_trabajador.rol == "admin" or current_trabajador.rol == "responsable" or current_trabajador.rol == "tecnic":
        respuesta, estacion = control.get_reservas_id(id)
        if ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "responsable" ) or ( estacion != current_trabajador.id_estacion and current_trabajador.rol == "tecnic" ):
            return jsonify({"error": "User not authorized."}), 401
        if respuesta: 
            deleted = control.remove_reserva(id)
            if deleted:
                return jsonify({"msg": "Data deleted correctly."}), 200
        else:
            return jsonify({"error": "Reserva not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
