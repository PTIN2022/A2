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
        estacion = request.json["estacion"]
        fecha_inicio = request.json["fecha_inicio"] # Dia y hora
        fecha_final = request.json["fecha_final"]
        fecha_final_str = datetime.strptime(fecha_final, '%d-%m-%Y %H:%M')
        fecha_inicio_str = datetime.strptime(fecha_inicio, '%d-%m-%Y %H:%M')
        matricula = request.json["matricula"]
        DNI = request.json["DNI"]
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


@reservas.route('/reservas/<id>', methods=["PUT"])
def modify_reserva(id):
    estacion = None
    desde = None
    hasta = None
    matricula = None
    data = None
    DNI = None

    # TODO: mirar bien si hay algo que no se esperaba o algo asi...
    if "estacion" in request.json:
        estacion = request.json["estacion"]
    if "desde" in request.json:
        desde = request.json["desde"]
    if "hasta" in request.json:
        hasta = request.json["hasta"]
    if "matricula" in request.json:
        matricula = request.json["matricula"]
    if "data" in request.json:
        try:
            data = request.json["data"]
            data = datetime.date(datetime.strptime(data, '%d-%m-%Y'))
        except ValueError:
            return jsonify({"error": "Malformed request syntax."}), 400
    if "DNI" in request.json:
        DNI = request.json["DNI"]
    if "plaza" in request.json:
        plaza = request.json["plaza"]
    respuesta = control.modify_reserva(id, estacion, desde, hasta, matricula, data, DNI, plaza)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404


@reservas.route('/reservas/byname/<estacion>', methods=["GET"])
def get_reserva_by_estacio(estacion):
    respuesta = control.get_reservas_estacion(estacion)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404


@reservas.route('/reservas/bymatricula/<matricula>', methods=["GET"])
def get_reserva_by_matricula(matricula):
    respuesta = control.get_reservas_matricula(matricula)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404


@reservas.route('/reservas/bydni/<dni>', methods=["GET"])
def get_reserva_by_dni(dni):
    respuesta = control.get_reservas_dni(dni)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404


@reservas.route('/reservas/<id>', methods=["DELETE"])
def deleted_reservas(id):
    deleted = control.remove_reserva(id)
    if deleted:
        return jsonify({"msg": "Data deleted correctly."}), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404
