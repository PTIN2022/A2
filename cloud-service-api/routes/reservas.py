import controller.reservasController as control
from flask import Blueprint, jsonify

reservas = Blueprint('reservas', __name__)


@reservas.route('/reservas', methods=['GET'])
def get_reservas():
    respuesta = control.get_all_reservas()
    return jsonify(respuesta)


@reservas.route('/reservas/<id_reserva>', methods=["GET"])
def get_reserva_by_id(id_reserva):
    respuesta = control.get_reservas_id(id_reserva)
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


@reservas.route('/reservas/bydni/<dni>', methods=["GET"])
def get_reserva_by_dni(dni):
    respuesta = control.get_reservas_dni(dni)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404


@reservas.route('/reservas/<id_reserva>', methods=["DELETE"])
def deleted_reservas(id_reserva):
    deleted = control.remove_reserva(id_reserva)
    if deleted:
        return jsonify({"msg": "Data deleted correctly."}), 200
    else:
        return jsonify({"error": "Reserva not found."}), 404

@reservas.route('/reservas/<id_reserva>', methods=["PUT"])
def put_reservas(id_reserva):
	estacion = None
	desde = None
	hasta = None
	matricula = None
	fecha = None
	DNI = None
	
	if "estacion" in request.json:
		estacion = request.json["estacion"]
	if "desde" in request.json:
		desde = request.json["desde"]
	if "hasta" in request.json:
		hasta = request.json["hasta"]
	if "matricula" in request.json:
		matricula = request.json["matricula"]
	if "fecha" in request.json:
		fecha = request.json["fecha"]
	if "DNI" in request.json:
		DNI = request.json["DNI"]
	
	respuesta = control.modify_reserva(id_reserva, estacion, desde, hasta, matricula, fecha, DNI)
	
	if respuesta:
		return jsonify(respuesta), 200
	else:
		return jsonify({"error": "User not found."}), 404
		
@reservas.route('/reservas', methods=["POST"])
def post_reservas():
	estacion = request.json["estacion"]
	desde = request.json["desde"]
	hasta = request.json["hasta"]
	matricula = request.json["matricula"]
	fecha = request.json["fecha"]
	DNI = request.json["DNI"]
	
	id = control.post_reserva(estacion, desde, hasta, matricula, fecha, DNI)
	
	respuesta = control.get_reservas_id(id)
	
	return jsonify(respuesta)
	
	
