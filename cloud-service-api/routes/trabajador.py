import json
import controller.trabajadorController as control

from utils import utils
from datetime import datetime
from flask import Blueprint, jsonify, request

trabajador = Blueprint('trabajadores', __name__)

@trabajador.route('/trabajador', methods=['POST'])
def post_trabajador():
    DNI = request.form.to_dict()["dni"]
    name = request.form.to_dict()["name"]
    lastname = request.form.to_dict()["lastname"]
    telf = request.form.to_dict()["telf"]
    email = request.form.to_dict()["email"]
    rol = request.form.to_dict()["rol"]
    last_access = -1
    picture = "https://editor.swagger.io/" #TODO: guardar imagen
    

    t = control.post_trabajador(DNI, name, lastname, telf, email, rol, last_access, picture)

    return jsonify(json.loads(t))
    
    '''print("holi")
    print(request.form.to_dict())
    print(request.files)
    return jsonify("")'''
