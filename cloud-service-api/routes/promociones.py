import controller.promocionesController as control

from flask import Blueprint, jsonify, request
from utils.utils import token_required

promociones = Blueprint('promociones', __name__)


@promociones.route('/promociones', methods=['GET'])
@token_required
def get_promocion(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        respuesta = control.get_all_promociones()
        return jsonify(respuesta)
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/<id_promo>', methods=['GET'])
@token_required
def get_promo_id(current_trabajador, id_promo):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        respuesta = control.get_promo_id(id_promo)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Promocion not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/estado/<estado>', methods=['GET'])
@token_required
def get_promo_by_estado(current_trabajador, estado):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        respuesta = control.get_promo_estado(estado)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Promocion not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/<id_promo>/estacion', methods=['GET'])
@token_required
def get_estacion_by_promo(current_trabajador, id_promo):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        if not control.Promociones.query.filter(control.Promociones.id_promo == id_promo).one_or_none():
            return jsonify({"error": "Promocion not found."}), 404
        respuesta = control.get_promo_estaciones(id_promo)
        if respuesta:
            return jsonify(Estacion=respuesta), 200
        else:
            return jsonify({"error": "Estaciones not found for this promo."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/estacion/<id_estacion>', methods=['GET'])
@token_required
def get_promo_by_estacion(current_trabajador, id_estacion):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        i = control.Estacion.query.filter(control.Estacion.id_estacion == id_estacion).one_or_none()
        if i:
            respuesta = control.get_promo_estacion(id_estacion)
            if respuesta:
                return jsonify(respuesta), 200
            else:
                return jsonify({"error": "Promociones not found for this Estacion."}), 400
        else:
            return jsonify({"error": "Estacion not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones', methods=['POST'])
@token_required
def post_promocion(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        estaciones = request.json["id_estaciones"]
        estaciones = estaciones.split("-")
        for estacion in estaciones:
            if not control.Estacion.query.filter(control.Estacion.id_estacion == estacion).one_or_none():
                return jsonify({"error": "Estacion not found."}), 404
        descuento = request.json["descuento"]
        fecha_inicio = request.json["fecha_inicio"]
        fecha_fin = request.json["fecha_fin"]
        descripcion = request.json["descripcion"]

        p = control.post_promociones(estaciones, descuento, fecha_inicio, fecha_fin, descripcion)
        if p:
            return jsonify(p), 200
        else:
            return jsonify({"error": "Malformed request syntax."}), 400
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/<id_promo>', methods=["PUT"])
@token_required
def modify_promocion(current_trabajador, id_promo):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        id_estacion = None
        descuento = None
        fecha_inicio = None
        fecha_fin = None
        descripcion = None
        cantidad_usados = None
        if "id_estacion" in request.json:
            i = control.Estacion.query.filter(control.Estacion.id_estacion == request.json["id_estacion"]).one_or_none()
            if i:
                id_estacion = request.json["id_estacion"]
            else:
                return jsonify({"error": "Estacion not found."}), 404
        if "descuento" in request.json:
            descuento = request.json["descuento"]
        if "fecha_inicio" in request.json:
            fecha_inicio = request.json["fecha_inicio"]
        if "fecha_fin" in request.json:
            fecha_fin = request.json["fecha_fin"]
        if "descripcion" in request.json:
            descripcion = request.json["descripcion"]
        if "cantidad_usados" in request.json:
            cantidad_usados = request.json["cantidad_usados"]

        respuesta = control.modify_promociones(id_promo, id_estacion, descuento, fecha_inicio, fecha_fin, descripcion, cantidad_usados)

        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Promocion not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/<id_promo>/<id_estacion>/activar', methods=["PUT"])
@token_required
def modificar_estado(current_trabajador, id_promo, id_estacion):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        i = control.Estacion.query.filter(control.Estacion.id_estacion == id_estacion).one_or_none()
        if not i:
            return jsonify({"error": "Estacion not found."}), 404
        if not control.Promociones.query.filter(control.Promociones.id_promo == id_promo).one_or_none():
            return jsonify({"error": "Promocion not found."}), 404
        respuesta = control.modify_estado(id_promo, id_estacion)
        if respuesta:
            return jsonify({"msg": "Promocion activated succesfully"}), 200
        else:
            return jsonify({"error": "Promocion not found for this estacion."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/<id_promo>', methods=["DELETE"])
@token_required
def deleted_promocion(current_trabajador, id_promo):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        deleted = control.delete_promocion(id_promo)
        if deleted:
            return jsonify({"msg": "Promocion deleted succesfully"}), 200
        else:
            return jsonify({"error": "Promocion not found."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones/<id_promo>/<id_estacion>', methods=["DELETE"])
@token_required
def deleted_estacion_from_promocion(current_trabajador, id_promo, id_estacion):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":
        i = control.Estacion.query.filter(control.Estacion.id_estacion == id_estacion).one_or_none()
        if not i:
            return jsonify({"error": "Estacion not found."}), 404
        if not control.Promociones.query.filter(control.Promociones.id_promo == id_promo).one_or_none():
            return jsonify({"error": "Promocion not found."}), 404
        deleted = control.delete_estacion_promocion(id_promo, id_estacion)
        if deleted:
            return jsonify({"msg": "Estacion deleted succesfully of Promocion"}), 200
        else:
            return jsonify({"error": "Estacion not found for this Promocion."}), 404
    else:
        return jsonify({"error": "User not authorized."}), 401
