from utils.db import db
from models.model import Vehiculo, VehiculoSchema
from models.model import Cliente
from models.model import Reserva
from models.model import Modelo, ModeloSchema

def get_all_vehiculos():
    i = Vehiculo.query.all()
    if i:
        return VehiculoSchema(many=True).dump(i)
        
    return None


def get_vehiculo_by_matricula(matricula):
    i = Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none()
    if i:
        vehiculo = VehiculoSchema().dump(i)
        m = Modelo.query.filter(Modelo.modelo == i.modelos).one_or_none()
        vehiculo["modelo"] = []
        vehiculo["modelo"].append(ModeloSchema().dump(m))
        return vehiculo
    
    return None


def post_vehiculo(matricula, modelo, porcentaje_bat):
    mod = Modelo.query.filter(Modelo.modelo == modelo).one_or_none()
    if mod:
        v = Vehiculo(matricula, porcentaje_bat, modelo)
        db.session.add(v)
        db.session.commit()
        return VehiculoSchema().dump(v)

    return None


def get_vehiculo_by_idcliente(id_cliente):
    i = Vehiculo.query.filter(Vehiculo.id_cliente == id_cliente)
    if i:
        Vehiculo_dict = VehiculoSchema().dump(i)
        return Vehiculo_dict

    return None


def delete_vehiculo_matr(matricula):
    i = Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False


def modify_vehiculo(matricula, porcentaje_bat):
    i = Vehiculo.query.filter(Vehiculo.matricula == matricula).one_or_none()
    if i:
        if porcentaje_bat:
            print ("aaa")
            i.porcentaje_bat = porcentaje_bat
            print ("ccccc", i.porcentaje_bat)
        db.session.commit()
        return VehiculoSchema().dump(i)
    return None
