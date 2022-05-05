from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.usuari_t import Usuari_t


class Trabajador(db.Model):
    id_trabajador = db.Column('id_usuari', db.ForeignKey('usuari_t.id_usuari'), nullable=False, primary_key=True)
    rol = db.Column(db.String(20), nullable=False)
    last_access = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    question = db.Column(db.String(300), nullable=False)

    def __init__(self, id_trabajador, rol, last_access, estado, question):
        self.id_trabajador = id_trabajador
        self.rol = rol
        self.last_access = last_access
        self.estado = estado
        self.question = question


class TrabajadorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trabajador
