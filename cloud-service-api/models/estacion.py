from utils.db import db
import models.plaza  # noqa: F401
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Estacion(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    estacion = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    kwh_max = db.Column(db.Integer, nullable=False)
    kwh_now = db.Column(db.Integer, nullable=False)
    ocupation_max = db.Column(db.Integer, nullable=False)
    ocupation_now = db.Column(db.Integer, nullable=False)
    surface_in_meters = db.Column(db.Integer, nullable=False)
    boss = db.Column(db.String(20), nullable=False)  # TODO: foreing key
    latitud = db.Column(db.Integer, nullable=False)
    longitud = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(320), nullable=False)
    plazas = db.relationship("Plaza",  backref="estacion")

    def __init__(self, estacion, direccion, kwh_max, kwh_now, ocupation_max, ocupation_now, surface_in_meters, boss, latitud, longitud, imagen):
        self.estacion = estacion
        self.direccion = direccion
        self.kwh_max = kwh_max
        self.kwh_now = kwh_now
        self.ocupation_max = ocupation_max
        self.ocupation_now = ocupation_now
        self.surface_in_meters = surface_in_meters
        self.latitud = latitud
        self.longitud = longitud
        self.imagen = imagen
        self.boss = boss


class EstacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Estacion
