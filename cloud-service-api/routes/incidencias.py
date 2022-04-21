import json
import controller.incidenciaController as control

from utils import utils
from datetime import datetime
from flask import Blueprint, jsonify, request

incidencias = Blueprint('incidencias', __name__)


@incidencias.route('/incidencias', methods=['GET'])
def get_incidencias():
    respuesta = control.get_all_incidencias()
    return jsonify(json.loads(respuesta))


@incidencias.route('/incidencias', methods=['POST'])
def post_incidencias():
    estacion = request.json["estacion"]
    direccion = request.json["direccion"]
    fecha_averia = request.json["fecha_averia"]
    fecha_averia = datetime.date(datetime.strptime(fecha_averia, '%d/%m/%Y'))
    descripcion = request.json["descripcion"]

    id = control.post_incidencia(estacion, direccion, fecha_averia, descripcion)

    respuesta = control.get_incidencias_id(id)
    return jsonify(respuesta)


@incidencias.route('/incidencias/<id>', methods=["GET"])
def get_incidencia_by_id(id):
    respuesta = control.get_incidencias_id(id)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Incidencia not found"}), 404


@incidencias.route('/incidencias/<id>', methods=["PUT"])
def modify_incidencia(id):
    estacion = None
    direccion = None
    fecha_averia = None
    descripcion = None
    estado = None

    # TODO: mirar bien si hay algo que no se esperaba o algo asi...
    if "estacion" in request.json:
        estacion = request.json["estacion"]
    if "direccion" in request.json:
        direccion = request.json["direccion"]
    if "fecha_averia" in request.json:
        fecha_averia = request.json["fecha_averia"]
        fecha_averia = datetime.date(datetime.strptime(fecha_averia, '%d/%m/%y'))

    if "descripcion" in request.json:
        descripcion = request.json["descripcion"]
    if "estado" in request.json:
        print(request.json["estado"])
        estado = utils.strtobool(str(request.json["estado"]))

    respuesta = control.modify_incidencia(id, estacion, direccion, fecha_averia, descripcion, estado)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Incidencia not found"}), 404


@incidencias.route('/incidencias/byname/<estacion>', methods=["GET"])
def get_incidencia_by_estacio(estacion):
    respuesta = control.get_incidencias_estacion(estacion)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Incidencia not found"}), 404


@incidencias.route('/incidencias/<id>', methods=["DELETE"])
def deleted_incidencias(id):
    deleted = control.deleted_incidencias(id)
    if deleted:
        return jsonify({"msg": "Data deleted correctly."}), 200
    else:
        return jsonify({"error": "Incidencia not found"}), 404
