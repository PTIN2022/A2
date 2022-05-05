from utils.db import db
from models.usuari_t import Usuari_t
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import models.aviso
import models.reserva

class Cliente(db.Model):
    id_cliente = db.Column('id_usuari', db.ForeignKey('usuari_t.id_usuari'), nullable=False, primary_key=True)
    avisos = db.relationship("Aviso",  backref="cliente")
    reservas = db.relationship("Reserva",  backref="cliente")

    def __init__(self, id_cliente):
        self.id_cliente = id_cliente

class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
