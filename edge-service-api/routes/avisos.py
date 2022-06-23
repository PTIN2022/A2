import controller.avisosController as control
from flask import Blueprint, jsonify, request
from utils.utils import token_required
from datetime import datetime

avisos = Blueprint('avisos', __name__)


@avisos.route('/avisos', methods=['GET'])
@token_required
def get_avisos(current_usuario):
    if current_usuario:
        respuesta = control.get_all_avisos()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@avisos.route('/avisos/byuser', methods=['GET'])
@token_required
def get_avisos_by_user(current_usuario):
    if current_usuario:
        respuesta = control.get_avisos_by_user(current_usuario)
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@avisos.route('/avisos', methods=['POST'])
@token_required
def post_avisos(current_usuario):
    # necesitamos id_reserva
    if current_usuario:
        id_reserva = None
        tipo = None
        texto = None
        if request.json["id_reserva"]:
            id_reserva = request.json["id_reserva"]
        else:
            return jsonify({"error": "Malformed request, needed id_reserva."}), 400
        if request.json["tipo"]:
            tipo = request.json["tipo"]
        else:
            return jsonify({"error": "Malformed request, needed tipo."}), 400
        if request.json["texto"]:
            texto = request.json["texto"]
        else:
            return jsonify({"error": "Malformed request, needed texto."}), 400

        respuesta = control.post_avisos(current_usuario.id_cliente, id_reserva, tipo, texto, datetime.now())
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Reserva not found or Reserva is not for User."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@avisos.route('/avisos/byreserva/<id_reserva>', methods=['GET'])
@token_required
def get_avisos_by_reserva(current_usuario, id_reserva):
    if current_usuario:
        respuesta = control.get_avisos_by_reserva(current_usuario.id_cliente, id_reserva)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Aviso not exist or there is not any aviso for that reserva and user "}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@avisos.route('/avisos/<id_aviso>', methods=['DELETE'])
@token_required
def delete_aviso(current_usuario, id_aviso):
    if current_usuario:
        respuesta = control.delete_aviso(current_usuario.id_cliente, id_aviso)
        if respuesta:
            return jsonify({"error": "Aviso deleted succesfully. "}), 200
        else:
            return jsonify({"error": "Aviso not exist or aviso is not for the user "}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@avisos.route('/avisos/<id_aviso>', methods=['PUT'])
@token_required
def modify_aviso(current_usuario, id_aviso):
    if current_usuario:
        if request.json["estado"]:
            estado = request.json["estado"]
        else:
            return jsonify({"error": "Malformed request, needed estado."}), 400
        respuesta = control.modify_aviso(current_usuario.id_cliente, id_aviso, estado)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Aviso not exist or aviso is not for the user "}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
