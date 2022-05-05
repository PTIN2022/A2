from utils.db import db
from models.cargador import Cargador
from models.horas import Horas
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class Consumo(db.Model):
    id_cargador = db.Column('id_cargador', db.ForeignKey('cargador.id_cargador'), nullable=False)
    id_horas = db.Column('id_horas', db.ForeignKey('horas.id'), nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint(id_cargador, id_horas),
        {},
    )

    def __init__(self, id_cargador, id_horas):
        self.id_cargador = id_cargador
        self.id_horas = id_horas

class ConsumoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Consumo