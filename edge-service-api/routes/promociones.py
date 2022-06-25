import controller.promocionesController as control
from flask import Blueprint, jsonify, request

promociones = Blueprint('promociones', __name__)


@promociones.route('/promociones', methods=['GET'])
def get_promocion():
    respuesta = control.get_all_promociones()
    return jsonify(respuesta), 200


@promociones.route('/promociones', methods=['POST'])
def post_promocion():
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


@promociones.route('/promociones/<id_promocion>', methods=['GET'])
def get_promo_id(id_promocion):
    respuesta = control.get_promo_id(id_promocion)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404


@promociones.route('/promociones/<id_promocion>', methods=["PUT"])
def modify_promocion(id_promocion):
    descuento = None
    fecha_inicio = None
    fecha_fin = None
    estado = False
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

    respuesta = control.modify_promociones(id_promocion, descuento, fecha_inicio, fecha_fin, estado, descripcion)

    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404


@promociones.route('/promociones/<id_promocion>', methods=["DELETE"])
def deleted_promocion(id_promocion):
    deleted = control.delete_promocion(id_promocion)
    if deleted:
        return jsonify({"msg": "Promocion deleted succesfully"}), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404


@promociones.route('/promociones/estado/<estado>', methods=['GET'])
def get_promo_by_estado(estado):
    respuesta = control.get_promo_estado(estado)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Malformed request syntax."}), 400


@promociones.route('/promociones/estaciones', methods=['GET'])
def get_promo_by_electrolineras():
    respuesta = control.get_promo_estaciones()
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Malformed request syntax."}), 400


@promociones.route('/promociones/estaciones/<id_estacion>', methods=['GET'])
def get_promo_by_electrolinera(id_estacion):
    respuesta = control.get_promo_estacion(id_estacion)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Malformed request syntax."}), 400