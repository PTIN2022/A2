from utils.db import db
from models.cargador import Cargador  # noqa: F401
from models.horas import Horas  # noqa: F401
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Consumo(db.Model):
    id_cargador = db.Column('id_cargador', db.ForeignKey('cargador.id_cargador'), nullable=False)
    id_horas = db.Column('id_horas', db.ForeignKey('horas.id'), nullable=False)
    potencia_consumida = db.Column(db.Integer, nullable=False)
    potencia_maxima = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint(id_cargador, id_horas),
        {},
    )

    def __init__(self, id_cargador, id_horas, potencia_consumida, potencia_maxima):
        self.id_cargador = id_cargador
        self.id_horas = id_horas
        self.potencia_consumida = potencia_consumida
        self.potencia_maxima = potencia_maxima


class ConsumoSchema(SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Consumo
