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
            return jsonify({"error": "Malformed request syntax."}), 400
    else:
        return jsonify({"error": "User not authorized."}), 401


@promociones.route('/promociones', methods=['POST'])
@token_required
def post_promocion(current_trabajador):
    if current_trabajador.cargo == "administrador" or current_trabajador.cargo == "encargado":

        descuento = request.form.to_dict()["descuento"]
        fecha_inicio = request.form.to_dict()["fecha_inicio"]
        fecha_fin = request.form.to_dict()["fecha_fin"]
        estado = request.form.to_dict()["estado"]
        descripcion = request.form.to_dict()["descripcion"]

        p = control.post_promociones(descuento, fecha_inicio, fecha_fin, estado, descripcion)
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

        descuento = None
        fecha_inicio = None
        fecha_fin = None
        estado = None
        descripcion = None

        if "descuento" in request.form.to_dict():
            descuento = request.form.to_dict()["descuento"]
        if "fecha_inicio" in request.form.to_dict():
            fecha_inicio = request.form.to_dict()["fecha_inicio"]
        if "fecha_fin" in request.form.to_dict():
            fecha_fin = request.form.to_dict()["fecha_fin"]
        if "estado" in request.form.to_dict():
            estado = request.form.to_dict()["estado"]
        if "descripcion" in request.form.to_dict():
            descripcion = request.form.to_dict()["descripcion"]

        respuesta = control.modify_promociones(id_promo, descuento, fecha_inicio, fecha_fin, estado, descripcion)

        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Promocion not found."}), 404
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
