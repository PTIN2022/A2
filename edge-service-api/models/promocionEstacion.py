from utils.db import db
from models.estacion import Estacion
from models.promocion import Promocion
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class PromocionEstacion(db.Model):
    id_estacion = db.Column('id_estacion', db.ForeignKey('estacion.id_estacion'), nullable=False)
    id_promo = db.Column('id_promo', db.ForeignKey('promocion.id_promo'), nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint(id_estacion, id_promo),
        {},
    )

    def __init__(self, id_estacion, id_promo):
        self.id_estacion = id_estacion
        self.id_promo = id_promo


class PromocionEstacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PromocionEstacion
