import controller.soporteController as control
from flask import Blueprint, jsonify, request

soporte = Blueprint('soporte', __name__)


@soporte.route('/soporte/<ticket_id>', methods=['GET'])
def get_soporte_ticket_id(ticket_id):
    respuesta = control.get_soporte_ticket_id(ticket_id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "User not found."}), 404


@soporte.route('/soporte', methods=['POST'])
def post_soporte():
    user_id = request.form.to_dict()["user_id"]
    ticket_id = request.form.to_dict()["ticket_id"]
    fecha = request.form.to_dict()["fecha"]
    descripcion = request.form.to_dict()["descripcion"]
    s = control.post_soporte(user_id, ticket_id, fecha, descripcion)
    return jsonify(s)


@soporte.route('/soporte/ticket_id/<user_id>', methods=['POST'])
def post_soporte_ticket_id_user_id(user_id):
    ticket_id = request.form.to_dict()["ticket_id"]
    user_id = request.form.to_dict()["user_id"]
    descripcion = request.form.to_dict()["descripcion"]
    fecha = request.form.to_dict()["fecha"]
    estado = request.form.to_dict()["estado"]
    mensaje = request.form.to_dict()["mensaje"]

    s = control.post_soporte_ticket_id_user_id(ticket_id, user_id, descripcion, fecha, estado, mensaje)
    return jsonify(s)


@soporte.route('/soporte/<ticket_id>', methods=["DELETE"])
def delete_soporte_ticket_id(ticket_id):
    deleted = control.delete_soporte_ticket_id(ticket_id)
    if deleted:
        return jsonify({"msg": "User deleted succesfully"}), 200
    else:
        return jsonify({"error": "User not found."}), 404
