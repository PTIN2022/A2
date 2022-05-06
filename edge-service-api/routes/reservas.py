import controller.reservasController as control
from utils import errors
from datetime import datetime
from flask import Blueprint, jsonify, request

reservas = Blueprint('reservas', __name__)


@reservas.route('/reservas', methods=['GET'])
def get_reservas():
    respuesta = control.get_all_reservas()
    return jsonify(respuesta)


@reservas.route('/reservas', methods=['POST'])
def post_reservas():
    try:
        print(request.json)
        estacion = int(request.json["id_estacion"])
        fecha_inicio = request.json["fecha_inicio"] # Dia y hora
        fecha_final = request.json["fecha_final"]
        fecha_final_str = datetime.strptime(fecha_final, '%d-%m-%Y %H:%M')
        fecha_inicio_str = datetime.strptime(fecha_inicio, '%d-%m-%Y %H:%M')
        matricula = request.json["id_vehiculo"]
        DNI = request.json["id_cliente"]
    
        #TODO: comprobar fecha final es mayor fecha inicial
        id = control.post_reserva(estacion, matricula, fecha_inicio_str, fecha_final_str, DNI)
        respuesta = control.get_reservas_id(id)
        return jsonify(respuesta)

    except ValueError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400
    except KeyError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400


@reservas.route('/reservas/<id>', methods=["GET"])
def get_reserva_by_id(id):
    respuesta = control.get_reservas_id(id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404


@reservas.route('/reservas/estacion/<id_estacion>', methods=["GET"])
def get_reserva_by_estacio(id_estacion):
    respuesta = control.get_reservas_estacion(id_estacion)
    return jsonify(respuesta), 200


@reservas.route('/reservas/bymatricula/<matricula>', methods=["GET"])
def get_reserva_by_matricula(matricula):
    respuesta = control.get_reservas_matricula(matricula)
    return jsonify(respuesta), 200


@reservas.route('/reservas/bydni/<dni>', methods=["GET"])
def get_reserva_by_dni(dni):
    respuesta = control.get_reservas_dni(dni)
    return jsonify(respuesta), 200


@reservas.route('/reservas/<id>', methods=["DELETE"])
def deleted_reservas(id):
    deleted = control.remove_reserva(id)
    if deleted:
        return jsonify({"msg": "Data deleted correctly."}), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404
