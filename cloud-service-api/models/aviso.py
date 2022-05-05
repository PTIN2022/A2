from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Aviso(db.Model):
    id_aviso = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    tipo = db.Column(db.String(20), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    hora = db.Column(db.DateTime, nullable=False)

    id_reserva = db.Column(db.Integer, db.ForeignKey("reserva.id_reserva"), nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey("cliente.id_usuari"), nullable=False)

    def __init__(self, tipo, texto, hora, id_reserva, id_cliente):  # need
        self.tipo = tipo
        self.texto = texto
        self.hora = hora
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente


class AvisoSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Aviso
