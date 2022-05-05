from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.mysql import FLOAT
import models.aviso

class Usuari_t(db.Model):

    id_usuari = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    dni = db.Column(db.String(15), nullable=False)
    foto = db.Column(db.String(15), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)


    def __init__(self, tipo, nombre, apellido, email,dni, foto, telefono, username,password):
        self.tipo = tipo
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.dni = dni
        self.foto = foto
        self.telefono = telefono
        self.username = username
        self.password = password

class Usuari_tSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Usuari_t