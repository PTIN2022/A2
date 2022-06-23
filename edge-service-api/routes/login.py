import controller.loginController as control
from utils import errors
from flask import Blueprint, jsonify, request
from utils.utils import token_required

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)


@login.route('/login', methods=['POST'])
def post_login():
    try:
        username = request.json["email"]
        password = request.json["password"]
        encoded_jwt, cliente = control.post_login(username, password)

        if encoded_jwt:
            return jsonify({'token': encoded_jwt, 'cliente': cliente}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 400
    except ValueError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400
    except KeyError as e:
        print(e)
        return jsonify(errors.malformed_error()), 400

@logout.route('/logout', methods=['GET'])
@token_required
def get_logout(current_usuario):
    if current_usuario:
        return jsonify({'message': 'You succesfully logged out'}), 200
    else:
        return jsonify({"error": "User not authorized."}), 401
