import controller.incidenciaController as control

from datetime import datetime
from utils import errors
from flask import Blueprint, jsonify, request
from utils.utils import token_required
from models.model import Estacion

incidencias = Blueprint('incidencias', __name__)


@incidencias.route('/incidencias', methods=['GET'])
@token_required
def get_incidencias(current_trabajador):
    if current_trabajador.cargo == "trabajador":
        e = Estacion.query.filter(Estacion.id_estacion == current_trabajador.id_estacion).one_or_none()
        respuesta = control.get_incidencias_estacion(e.nombre_est)
    elif current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        respuesta = control.get_all_incidencias()
    return jsonify(respuesta)


@incidencias.route('/incidencias', methods=['POST'])
@token_required
def post_incidencias(current_trabajador):
    try:
        estacion = request.json["estacion"]
        if current_trabajador.cargo == "trabajador":
            e = Estacion.query.filter(Estacion.id_estacion == current_trabajador.id_estacion).one_or_none()
            if e.nombre_est != estacion:
                return jsonify({"error": "User not authorized."}), 401
        estado = request.json["estado"]
        fecha_averia = request.json["fecha_averia"]
        fecha_averia = datetime.date(datetime.strptime(fecha_averia, '%Y-%m-%d'))
        descripcion = request.json["descripcion"]
        if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
            id = control.post_incidencia(estacion, fecha_averia, descripcion, estado)
            respuesta = control.get_incidencias_id(id)
        else:
            return jsonify({"error": "User not authorized."}), 401
        return jsonify(respuesta)

    except ValueError:
        return jsonify(errors.malformed_error()), 400
    except KeyError:
        return jsonify(errors.malformed_error()), 400


@incidencias.route('/incidencias/<id>', methods=["GET"])
@token_required
def get_incidencia_by_id(current_trabajador, id):
    respuesta = control.get_incidencias_id(id)
    if current_trabajador.cargo == "trabajador":
        e = Estacion.query.filter(Estacion.id_estacion == current_trabajador.id_estacion).one_or_none()
        if respuesta["name_estacion"] != e.nombre_est:
            return jsonify({"error": "User not authorized."}), 401
    if respuesta and (current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador"):
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Incidencia not found."}), 404


@incidencias.route('/incidencias/<id>', methods=["PUT"])
@token_required
def modify_incidencia(current_trabajador, id):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        estacion = None
        trabajador = None
        fecha_averia = None
        descripcion = None
        estado = None
        respuesta = control.get_incidencias_id(id)
        if current_trabajador.cargo == "trabajador":
            e = Estacion.query.filter(Estacion.id_estacion == current_trabajador.id_estacion).one_or_none()
            if respuesta:
                if respuesta["name_estacion"] != e.nombre_est:
                    return jsonify({"error": "User not authorized."}), 401
            else:
                return jsonify({"error": "Incidencia not found."}), 404
        # TODO: mirar bien si hay algo que no se esperaba o algo asi...
        if "estacion" in request.json:
            estacion = request.json["estacion"]
            if current_trabajador.cargo == "trabajador":
                e = Estacion.query.filter(Estacion.id_estacion == current_trabajador.id_estacion).one_or_none()
                if estacion != e.nombre_est:
                    return jsonify({"error": "User not authorized."}), 401

        if "fecha_averia" in request.json:
            try:
                fecha_averia = request.json["fecha_averia"]
                fecha_averia = datetime.date(datetime.strptime(fecha_averia, '%Y-%m-%d'))
            except ValueError:
                return jsonify({"error": "Malformed request syntax."}), 400

        if "trabajador" in request.json:
            trabajador = request.json["trabajador"]
        if "estado" in request.json:
            estado = str(request.json["estado"])
        if "descripcion" in request.json:
            descripcion = str(request.json["descripcion"])

        respuesta = control.modify_incidencia(id, estacion, fecha_averia, descripcion, estado, trabajador)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Incidencia not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@incidencias.route('/incidencias/byname/<estacion>', methods=["GET"])
@token_required
def get_incidencia_by_estacio(current_trabajador, estacion):
    if current_trabajador.cargo == "trabajador":
        e = Estacion.query.filter(Estacion.id_estacion == current_trabajador.id_estacion).one_or_none()
        if estacion != e.nombre_est:
            return jsonify({"error": "User not authorized."}), 401
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        respuesta = control.get_incidencias_estacion(estacion)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Incidencia not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@incidencias.route('/incidencias/<id>', methods=["DELETE"])
@token_required
def deleted_incidencias(current_trabajador, id):
    respuesta = control.get_incidencias_id(id)
    if current_trabajador.cargo == "trabajador":
        e = Estacion.query.filter(Estacion.id_estacion == current_trabajador.id_estacion).one_or_none()
        if respuesta:
            if respuesta["name_estacion"] != e.nombre_est:
                return jsonify({"error": "User not authorized."}), 401
        else:
            return jsonify({"error": "Incidencia not found."}), 404
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado" or current_trabajador.cargo == "trabajador":
        deleted = control.remove_incidencia(id)
        if deleted:
            return jsonify({"msg": "Data deleted correctly."}), 200
        else:
            return jsonify({"error": "Incidencia not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
