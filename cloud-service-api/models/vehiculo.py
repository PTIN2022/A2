from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Vehiculo(db.Model):
    id_vehiculo = db.Column(db.String(20), nullable=False, primary_key=True)
    capacidad = db.Column(db.Integer, nullable=False)
    potencia_carga = db.Column(db.Integer, nullable=False)
    modelo = db.Column(db.String(30), nullable=False)
    procentaje_bat = db.Column(db.Integer, nullable=False)

    #reservas = db.relationship("Reserva",  backref="vehiculo")

    def __init__(self, matricula, capacidad, potencia_carga, modelo, procentaje_bat):
        self.matricula = matricula
        self.capacidad = capacidad
        self.potencia_carga = potencia_carga
        self.modelo = modelo
        self.procentaje_bat = procentaje_bat


class VehiculoSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Vehiculo
