import controller.loginController as control

from flask import Blueprint, jsonify, request
from utils.utils import token_required

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)


@login.route('/login', methods=['POST'])
def post_login():
    username = request.form.to_dict()["email"]
    password = request.form.to_dict()["password"]

    encoded_jwt, id_cliente = control.post_login(username, password)

    if encoded_jwt:
        return jsonify({'token': encoded_jwt, 'id_cliente': id_cliente}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 400


@logout.route('/logout', methods=['GET'])
@token_required
def get_logout(current_usuario):
    if current_usuario:
        return jsonify({'message': 'You succesfully logged out'}), 200
    else:
        return jsonify({"error": "User not authorized."}), 401
