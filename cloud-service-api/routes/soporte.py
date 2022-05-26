import controller.soporteController as control
from flask import Blueprint, jsonify, request
from datetime import datetime
from utils import errors

soporte = Blueprint('soporte', __name__)


@soporte.route('/soporte', methods=['GET'])
def get_soporte():
    respuesta = control.get_all_soporte()
    return jsonify(respuesta)


@soporte.route('/soporte', methods=['POST'])
def post_soporte():
    try:
        fecha = datetime.now()
        descripcion = request.json["descripcion"]
        estado = request.json["estado"]
        id_cliente = request.json["cliente"]
        asunto = request.json["asunto"]
        ticket_id = control.post_soporte(descripcion, fecha, estado, id_cliente, asunto)
        ticket = control.get_soporte_ticket_id(ticket_id)
        return jsonify(ticket), 200

    except ValueError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400
    except KeyError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400


@soporte.route('/soporte/<ticket_id>', methods=['GET'])
def get_soporte_ticket_id(ticket_id):
    respuesta = control.get_soporte_ticket_id(ticket_id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Ticket not found."}), 404


@soporte.route('/soporte/<ticket_id>', methods=["DELETE"])
def delete_soporte_ticket_id(ticket_id):
    deleted = control.delete_soporte_ticket_id(ticket_id)
    if deleted:
        return jsonify({"msg": "Ticket deleted succesfully."}), 200
    else:
        return jsonify({"error": "Ticket not found."}), 404


@soporte.route('/soporte/<ticket_id>', methods=['POST'])
def post_soporte_by_ticket(ticket_id):
    try:
        mensaje = request.form.to_dict()["mensaje"]
        fecha = datetime.now()
        id_cliente =request.form.to_dict()["cliente"]
        resultado = control.post_soporte_by_ticket(mensaje, fecha, ticket_id, id_cliente)
        if resultado:
            respuesta = control.get_soporte_ticket_id(ticket_id)
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Ticket not found."}), 400
    except ValueError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400
    except KeyError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400


@soporte.route('/soporte/byuser/<user_id>', methods=["GET"])
def get_soporte_user_id(user_id):
    messages = control.get_soporte_user_id(user_id)
    if messages:
        return jsonify(messages), 200
    else:
        return jsonify({"error": "Ticket not found."}), 404


@soporte.route('/soporte/delete_missage/<msg_id>', methods=['DELETE'])
def delete_message_by_user(ticket_id, msg_id):
    respuesta = control.delete_message_by_user(ticket_id, msg_id)
    if respuesta:
        return jsonify({"msg": "Message deleted succesfully."}), 200
    else:
        return jsonify({"error": "Message not found."}), 404
