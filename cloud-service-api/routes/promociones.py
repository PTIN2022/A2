import controller.promocionesController as control
from flask import Blueprint, jsonify, request

promociones = Blueprint('promociones', __name__)


@promociones.route('/promociones', methods=['GET'])
def get_promocion():
    respuesta = control.get_all_promociones()
    return jsonify(respuesta)


@promociones.route('/promociones/<id_promo>', methods=['GET'])
def get_promo_id(id_promo):
    respuesta = control.get_promo_id(id_promo)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404


@promociones.route('/promociones/estacion/<id_estacion>', methods=['GET'])
def get_promo_by_esaction(id_estacion):
    respuesta = control.get_promo_estacion(id_estacion)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Bad syntax."}), 404


@promociones.route('/promociones/estado/<estado>', methods=['GET'])
def get_promo_by_estado(estado):
    respuesta = control.get_promo_estado(estado)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Bad syntax."}), 404


@promociones.route('/promociones', methods=['POST'])
def post_promocion():
    descuento = request.form.to_dict()["descuento"]
    cantidad_cupones = request.form.to_dict()["cantidad_cupones"]
    cantidad_usados = request.form.to_dict()["cantidad_usados"]
    fecha_inicio = request.form.to_dict()["fecha_inicio"]
    fecha_fin = request.form.to_dict()["fecha_fin"]
    estado = request.form.to_dict()["estado"]
    id_estacion = request.form.to_dict()["id_estacion"]
    descripcion = request.form.to_dict()["descripcion"]

    p = control.post_promociones(descuento, cantidad_cupones, cantidad_usados, fecha_inicio, fecha_fin, estado, id_estacion, descripcion)
    if p:
        return jsonify(p), 200
    else:
        return jsonify({"error": "Bad syntax."}), 404


@promociones.route('/promociones/<id_promo>', methods=["PUT"])
def modify_promocion(id_promo):
    descuento = None
    cantidad_cupones = None
    cantidad_usados = None
    fecha_inicio = None
    fecha_fin = None
    estado = None
    id_estacion = None
    descripcion = None


    if "descuento" in request.form.to_dict():
        descuento = request.form.to_dict()["descuento"]
    if "cantidad_cupones" in request.form.to_dict():
        cantidad_cupones = request.form.to_dict()["cantidad_cupones"]
    if "cantidad_usados" in request.form.to_dict():
        cantidad_usados = request.form.to_dict()["cantidad_usados"]
    if "fecha_inicio" in request.form.to_dict():
        fecha_inicio = request.form.to_dict()["fecha_inicio"]
    if "fecha_fin" in request.form.to_dict():
        fecha_fin = request.form.to_dict()["fecha_fin"]
    if "estado" in request.form.to_dict():
        estado = request.form.to_dict()["estado"]
    if "id_estacion" in request.form.to_dict():
        id_estacion = request.form.to_dict()["id_estacion"]
    if "descripcion" in request.form.to_dict():
        descripcion = request.form.to_dict()["descripcion"]

    respuesta = control.modify_promociones(id_promo, descuento, cantidad_cupones, cantidad_usados, fecha_inicio, fecha_fin, estado, id_estacion, descripcion)

    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404


@promociones.route('/promociones/<id_promo>', methods=["DELETE"])
def deleted_promocion(id_promo):
    deleted = control.delete_promocion(id_promo)
    if deleted:
        return jsonify({"msg": "Promocion deleted succesfully"}), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404
