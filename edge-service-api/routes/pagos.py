import controller.pagosController as pagos
from flask import Blueprint, jsonify, request
from utils.utils import token_required
from datetime import datetime

pagos = Blueprint('pagos', __name__)


@pagos.route('/transacciones', methods=['GET'])
@token_required
def get_all_transacciones(current_usuario):
    if current_usuario:
        respuesta = control.get_all_transacciones()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@pagos.route('/transacciones/cliente', methods=['GET'])
@token_required
def get_transacciones_by_clientes(current_usuario):
    # necesitamos id_reserva
    if current_usuario:
        respuesta = control.get_transacciones_by_clientes(current_usuario.id_cliente, id_reserva)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Error unexpected. May client doesn't exist. "}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401

@pagos.route('/transacciones/cliente/<id_reserva>', methods=['POST'])
@token_required
def post_transacciones_by_reservas(current_usuario, id_reserva):
    if current_usuario:
        tipo = None
        importe = None
        if request.json["tipo"]:
            tipo = request.json["tipo"]
        else:
            return jsonify({"error": "Malformed request, needed tipo."}), 400
        if request.json["importe"]:
            importe = request.json["importe"]
        else:
            return jsonify({"error": "Malformed request, needed texto."}), 400

        respuesta = control.post_transacciones_by_reservas(current_usuario.id_cliente, importe, tipo, id_reserva)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Reserva not found or Reserva is not for User."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401

@pagos.route('/saldo/cliente', methods=['GET'])
@token_required
def get_saldo_by_cliente(current_usuario):
    if current_usuario:
        return ({"saldo": current_usuario.saldo}), 200
    else:
        return jsonify({"error": "User not authorized."}), 401