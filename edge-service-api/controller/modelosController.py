from utils.db import db
from models.model import Modelo, ModeloSchema

def get_all_modelos():
    i = Modelo.query.all()
    if i:
        return ModeloSchema(many=True).dump(i)
        
    return None


def post_modelo(modelo, marca, potencia_carga, capacidad):
    mod = Modelo(modelo, marca, potencia_carga, capacidad)
    db.session.add(mod)
    db.session.commit()
    return ModeloSchema().dump(mod)
