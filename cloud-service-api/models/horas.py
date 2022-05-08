from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Horas(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    dia = db.Column(db.DateTime, nullable=False)
    hora = db.Column(db.DateTime, nullable=False)
    id_cargador = db.Column(db.Integer, db.ForeignKey("cargador.id_cargador"), nullable=False)

    def __init__(self, dia, hora, id_cargador):
        self.dia = dia
        self.hora = hora
        self.id_cargador = id_cargador


class HorasSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        model = Horas
