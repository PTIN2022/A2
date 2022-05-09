import controller.loginController as control

from flask import Blueprint, jsonify, request
from utils import utils, errors

login = Blueprint('login', __name__)
logout = Blueprint('logout', __name__)


@login.route('/login', methods=['POST'])
def post_login():
    username = request.form.to_dict()["username"]
    password = request.form.to_dict()["password"]

    encoded_jwt = control.post_login(username, password)
    
    if encoded_jwt:
        return jsonify({'token': encoded_jwt}), 200
    else:
        return jsonify({'error' : 'Invalid credentials'}), 400


@logout.route('/logout', methods=['GET'])
def get_logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message' : 'You succesfully logged out'}), 200
