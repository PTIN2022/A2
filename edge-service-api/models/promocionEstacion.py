from utils.db import db
from models.estacion import Estacion  # noqa: F401
from models.promociones import Promocion  # noqa: F401
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class PromocionEstacion(db.Model):
    id_estacion = db.Column('id_estacion',db.Integer, nullable=False, primary_key=True)
    id_promo = db.Column('id_promo',db.Integer, nullable=False, primary_key=True)
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
