import controller.soporteController as control
from flask import Blueprint, jsonify, request
from datetime import datetime
from utils import errors
from utils.utils import token_required

soporte = Blueprint('soporte', __name__)


@soporte.route('/soporte', methods=['GET'])
@token_required
def get_soporte(current_usuario):
    if current_usuario:
        respuesta = control.get_all_soporte()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@soporte.route('/soporte', methods=['POST'])
@token_required
def post_soporte(current_usuario):
    if current_usuario:
        try:
            descripcion = request.json["descripcion"]
            asunto = request.json["asunto"]
            ticket_id = control.post_soporte(descripcion, datetime.now(), current_usuario.id_cliente, asunto)
            if type(ticket_id) == dict:
                return jsonify(ticket_id), 400
            ticket = control.get_soporte_ticket_id(current_usuario.id_cliente, ticket_id)
            return jsonify(ticket), 200

        except ValueError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
        except KeyError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
    else:
        return jsonify({"error": "User not authorized."}), 401



@soporte.route('/soporte/<ticket_id>', methods=['GET'])
@token_required
def get_soporte_ticket_id(current_usuario, ticket_id):
    if current_usuario:
        respuesta = control.get_soporte_ticket_id(current_usuario.id_cliente, ticket_id)
        if respuesta == 0:
            return jsonify({ "error": "Ticket not exist or ticket is not from the user "}), 400
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Ticket not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@soporte.route('/soporte/<ticket_id>', methods=["DELETE"])
@token_required
def delete_soporte_ticket_id(current_usuario, ticket_id):
    if current_usuario:
        deleted = control.delete_soporte_ticket_id(current_usuario.id_cliente, ticket_id)
        if deleted:
            return jsonify({"msg": "Ticket deleted succesfully."}), 200
        else:
            return jsonify({"error": "Ticket not found or Ticket is not from the user."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401

@soporte.route('/soporte/<ticket_id>', methods=['POST'])
@token_required
def post_soporte_by_ticket(current_usuario, ticket_id):
    if current_usuario:
        try:
            mensaje = request.form.to_dict()["mensaje"]
            resultado = control.post_soporte_by_ticket(mensaje, datetime.now(), ticket_id, current_usuario.id_cliente)
            if resultado == 0:
                return jsonify({"error": "Ticket not found or Ticket is not from the user."}), 400
            if resultado:
                respuesta = control.get_soporte_ticket_id(current_usuario.id_cliente, ticket_id)
                return jsonify(respuesta), 200
            else:
                return jsonify({"error": "Ticket not found."}), 400
        except ValueError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
        except KeyError as e:
            print(e)
            return jsonify(errors.malformed_error()), 400
    else:
        return jsonify({"error": "User not authorized."}), 401


@soporte.route('/soporte/byuser', methods=["GET"])
@token_required
def get_soporte_user_id(current_usuario):
    if current_usuario:
        messages = control.get_soporte_user_id(current_usuario.id_cliente)
        if messages:
            return jsonify(messages), 200
        else:
            return jsonify({"error": "Ticket not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@soporte.route('/soporte/delete_missage/<ticket_id>/<msg_id>', methods=['DELETE'])
@token_required
def delete_message_by_user(current_usuario, ticket_id, msg_id):
    if current_usuario:
        respuesta = control.delete_message_by_user(current_usuario.id_cliente, ticket_id, msg_id)
        if respuesta:
            return jsonify({"msg": "Message deleted succesfully."}), 200
        else:
            return jsonify({"error": "Message not found or Message is not from the user."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401