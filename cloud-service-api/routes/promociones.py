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


@promociones.route('/promociones/estado/<estado>', methods=['GET'])
def get_promo_by_estado(estado):
    respuesta = control.get_promo_estado(estado)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404


@promociones.route('/promociones/<id_promo>/estacion', methods=['GET'])
def get_estacion_by_promo(id_promo):
    respuesta = control.get_promo_estaciones(id_promo)
    if respuesta:
        return jsonify(respuesta), 200
    else:
        return jsonify({"error": "Promocion not found."}), 404


@promociones.route('/promociones/estacion/<id_estacion>', methods=['GET'])
def get_promo_by_estacion(id_estacion):
    i = control.Estacion.query.filter(control.Estacion.id_estacion == id_estacion).one_or_none()
    if i:
        respuesta = control.get_promo_estacion(id_estacion)
        if respuesta:
            return jsonify(respuesta), 200
        else:
            return jsonify({"error": "Promociones not found for this Estacion."}), 400
    else:
        return jsonify({"error": "Estacion not found."}), 404


@promociones.route('/promociones', methods=['POST'])
def post_promocion():
    id_estacion = request.json["id_estacion"]
    i = control.Estacion.query.filter(control.Estacion.id_estacion == id_estacion).one_or_none()
    if i:
        descuento = request.json["descuento"]
        fecha_inicio = request.json["fecha_inicio"]
        fecha_fin = request.json["fecha_fin"]
        estado = request.json["estado"]
        descripcion = request.json["descripcion"]

        p = control.post_promociones(id_estacion, descuento, fecha_inicio, fecha_fin, estado, descripcion)
        if p:
            return jsonify(p), 200
        else:
            return jsonify({"error": "Malformed request syntax."}), 400
    else:
        return jsonify({"error": "Estacion not found."}), 404


@promociones.route('/promociones/<id_promo>', methods=["PUT"])
def modify_promocion(id_promo):
    id_estacion = None
    descuento = None
    fecha_inicio = None
    fecha_fin = None
    estado = None
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
    if "estado" in request.json:
        estado = request.json["estado"]
    if "descripcion" in request.json:
        descripcion = request.json["descripcion"]
    if "cantiddad_usados" in request.json:
        descripcion = request.json["cantiddad_usados"]

    respuesta = control.modify_promociones(id_promo, id_estacion, descuento, fecha_inicio, fecha_fin, estado, descripcion, cantiddad_usados)

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
