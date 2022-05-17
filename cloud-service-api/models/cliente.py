from utils.db import db
from models.usuari_t import Usuari_t  # noqa: F401
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import models.aviso  # noqa: F401
import models.reserva  # noqa: F401


class Cliente(db.Model):
    # avisos = db.relationship("Aviso",  backref="cliente")
    # id_usuari = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuari = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    # tipo = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    dni = db.Column(db.String(15), nullable=False)
    foto = db.Column(db.String(15), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    reservas = db.relationship("Reserva",  backref="cliente")

    def __init__(self, nombre, apellido, email, dni, foto, telefono, username, password):
        # self.tipo = tipo
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.dni = dni
        self.foto = foto
        self.telefono = telefono
        self.username = username
        self.password = password


class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
