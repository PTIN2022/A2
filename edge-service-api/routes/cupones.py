from flask import Blueprint, jsonify, request
from utils.utils import token_required
from controller.cuponesController import get_cupones_user, add_cupon_user, set_cupon_estado, check_cupon_user

cupones = Blueprint('cupones', __name__)


@cupones.route('/cupones', methods=['GET'])
@token_required
def get_cupones(current_usuario):
    print(current_usuario.id_usuari)
    return jsonify(get_cupones_user(current_usuario.id_usuari)), 200


@cupones.route('/cupones/<id_user>', methods=['POST'])
def post_cupones(id_user):
    cupon = request.json["cupon"]  # Dia y hora
    descuento = request.json["descuento"]
    c = add_cupon_user(descuento, cupon, id_user)
    if "error" in c:
        return jsonify(c), 404

    return jsonify(c), 200


@cupones.route('/cupones/<id_cupon>', methods=['PUT'])
@token_required
def set_estado(current_usuario, id_cupon):
    if current_usuario:
        estado = request.json["estado"]  # Dia y hora
        c = set_cupon_estado(id_cupon, estado)
        if "error" in c:
            return jsonify(c), 404
        return jsonify(c), 200
    else:
        return jsonify({"error": "User not authorized."}), 401


@cupones.route('/cupones/<id_cupon>', methods=['GET'])
@token_required
def check_cupon(current_usuario, id_cupon):
    c = check_cupon_user(id_cupon, current_usuario.id_usuari)
    if "error" in c:
        return jsonify(c), 404

    return jsonify(c), 200
