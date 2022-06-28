from utils.db import db
from models.model import Vehiculo, VehiculoSchema
from models.model import Modelo, ModeloSchema
from utils.mqtt_utils import send_to_cloud


def get_all_vehiculos():
    i = Vehiculo.query.all()
    if i:
        return VehiculoSchema(many=True).dump(i)
    return None


def get_vehiculo_by_matricula(cliente, matricula):
    i = Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none()
    if i:
        if i in cliente.vehiculos:
            vehiculo = VehiculoSchema().dump(i)
            mod = Modelo.query.filter(Modelo.modelo == i.modelos).one_or_none()
            vehiculo["modelo"] = []
            vehiculo["modelo"].append(ModeloSchema().dump(mod))
            return vehiculo
        return None
    return None


def post_vehiculo(cliente, matricula, modelo, porcentaje_bat):
    mod = Modelo.query.filter(Modelo.modelo == modelo).one_or_none()
    if mod:
        if Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none() is None:
            v = Vehiculo(matricula, porcentaje_bat, modelo)
            cliente.vehiculos.append(v)
            db.session.add(v)
            db.session.commit()
            vehiculo = VehiculoSchema().dump(v)
            vehiculo["modelo"] = []
            vehiculo["modelo"].append(ModeloSchema().dump(mod))

            payload = VehiculoSchema().dump(v)
            payload["cliente"] = cliente.dni
            payload["modelo"] = modelo
            send_to_cloud("gesys/cloud/clientes/vehiculo", payload)
            return vehiculo
        return {"error": "vehiculo ya existente"}

    return {"error": "modelo inexistente"}


def get_vehiculo_by_idcliente(cliente):
    if cliente:
        v = cliente.vehiculos
        aux = []
        for i in v:
            vehiculo = VehiculoSchema().dump(i)
            mod = Modelo.query.filter(Modelo.modelo == i.modelos).one_or_none()
            vehiculo["modelo"] = []
            vehiculo["modelo"].append(ModeloSchema().dump(mod))
            aux.append(vehiculo)

        return aux

    return None


def delete_vehiculo_matr(matricula):
    i = Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False


def modify_vehiculo(cliente, matricula, porcentaje_bat):
    i = Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none()
    if i:
        if porcentaje_bat:
            i.procentaje_bat = porcentaje_bat
        db.session.commit()
        return VehiculoSchema().dump(i)
    return None
