from utils.db import db
import models.cargador  # noqa: F401
import models.promocion  # noqa: F401
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Estacion(db.Model):

    id_estacion = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    nombre_est = db.Column(db.String(20), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    potencia_contratada = db.Column(db.Integer, nullable=False)
    zona = db.Column(db.Integer, nullable=False)
    ocupacion_actual = db.Column(db.Integer, nullable=False)
    potencia_usada = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(12), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    cargadores = db.relationship("Cargador", backref="estacion")

    def __init__(self, estacion, latitud, longitud, capacidad, direccion, potencia_contratada, zona, ocupacion_actual, potencia_usada, telefono, ciudad, pais):
        self.nombre_est = estacion
        self.latitud = latitud
        self.longitud = longitud
        self.capacidad = capacidad
        self.direccion = direccion
        self.potencia_contratada = potencia_contratada
        self.zona = zona
        self.ocupacion_actual = ocupacion_actual
        self.potencia_usada = potencia_usada
        self.telefono = telefono
        self.ciudad = ciudad
        self.pais = pais


class EstacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Estacion
