import controller.soporteController as control
from flask import Blueprint, jsonify, request

soporte = Blueprint('soporte', __name__)


@soporte.route('/soporte', methods=['GET'])
def get_soporte():
    respuesta = control.get_all_soporte()
    return jsonify(respuesta)


@soporte.route('/soporte/ticket_id/<user_id>', methods=['GET'])
def get_soporte_user_id(user_id):
    respuesta = control.get_soporte_user_id(user_id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "User not found."}), 404


@soporte.route('/soporte/<ticket_id>', methods=['GET'])
def get_soporte_ticket_id(ticket_id):
    respuesta = control.get_soporte_ticket_id(ticket_id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Ticket not found."}), 404


@soporte.route('/soporte/ticket_id/<user_id>', methods=['POST'])
def post_soporte_user_id():
    try:
        print(request.json)
        mensaje = request.json["mensaje"]
        fecha = request.json["fecha"]

        user_id = control.post_soporte_user_id(mensaje, fecha)
        respuesta = control.get_soporte_user_id(user_id)
        return jsonify(respuesta)

    except ValueError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400
    except KeyError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400


@soporte.route('/soporte', methods=['POST'])
def post_soporte():
    try:
        fecha = request.json["fecha"]
        fecha = datetime.date(datetime.strptime(fecha, '%Y-%m-%d'))
        descripcion = request.json["descripcion"]
        ticket_id = control.post_soporte(fecha, descripcion)

        respuesta = control.get_soporte_ticket_id(ticket_id)
        return jsonify(respuesta)

    except ValueError:
        return jsonify(errors.malformed_error()), 400
    except KeyError:
        return jsonify(errors.malformed_error()), 400


@soporte.route('/soporte/<ticket_id>', methods=["DELETE"])
def delete_soporte_ticket_id(ticket_id):
    deleted = control.delete_soporte_ticket_id(ticket_id)
    if deleted:
        return jsonify({"msg": "User deleted succesfully"}), 200
    else:
        return jsonify({"error": "User not found."}), 404
