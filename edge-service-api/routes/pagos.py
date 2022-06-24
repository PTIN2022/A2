import controller.pagosController as control
from flask import Blueprint, jsonify, request
from utils.utils import token_required
from utils import errors
from utils.db import db

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
        respuesta = control.get_transacciones_by_clientes(current_usuario)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Error unexpected. May Reserva doesn't exist. "}), 404
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

        respuesta = control.post_transacciones_by_reservas(current_usuario, importe, tipo, id_reserva)
        if respuesta:
            return jsonify(respuesta), 200
        elif respuesta == 0:
            return jsonify({"error": "Already exist a transaction done between the client and reserva. "}), 402
        else:
            return jsonify({"error": "Reserva not found or Reserva is not for User."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@pagos.route('/saldo', methods=['GET'])
@token_required
def get_saldo_by_cliente(current_usuario):
    if current_usuario:
        return ({"saldo": current_usuario.saldo}), 200
    else:
        return jsonify({"error": "User not authorized."}), 401


@pagos.route('/saldo', methods=['PUT'])
@token_required
def put_saldo_by_cliente(current_usuario):
    if current_usuario:
        try:
            type = request.json["type"]
            saldo = request.json["saldo"]  # Dia y hora
            if str(type) == "add":
                current_usuario.saldo += saldo
            else:
                current_usuario.saldo -= saldo
            db.session.commit()
            return ({"saldo": current_usuario.saldo}), 200
        
        except ValueError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
        except KeyError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
    else:
        return jsonify({"error": "User not authorized."}), 401

