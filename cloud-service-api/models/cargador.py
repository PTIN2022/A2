from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import models.reserva  # noqa: F401
import models.horas  # noqa: F401


class Cargador(db.Model):

    id_cargador = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    estado = db.Column(db.String(30), nullable=False)
    posicion = db.Column(db.String(80), nullable=False)
    estacion_id = db.Column(db.Integer, db.ForeignKey("estacion.id_estacion"), nullable=False)
    reservas = db.relationship("Reserva",  backref="cargador")
    horas = db.relationship("Horas",  backref="cargador")

    def __init__(self,  estado, posicion, estacion_id):
        self.estado = estado
        self.posicion = posicion
        self.estacion_id = estacion_id


class CargadorSchema(SQLAlchemyAutoSchema):
    # estacion= fields.Nested(EstacionSchema)
    class Meta:
        include_fk = True
        model = Cargador
