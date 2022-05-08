from utils.db import db
from models.reserva import Reserva  # noqa: F401
from models.cliente import Cliente  # noqa: F401
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Pago(db.Model):
    id_pago = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_reserva = db.Column('id_reserva', db.ForeignKey('reserva.id_reserva'), nullable=False)
    id_cliente = db.Column('id_cliente', db.ForeignKey('cliente.id_usuari'), nullable=False)
    __table_args__ = (
        db.UniqueConstraint(id_reserva, id_cliente),
        {},
    )
    estado = db.Column(db.String(30), nullable=False)

    def __init__(self, id_reserva, id_cliente, estado):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.estado = estado


class PagoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pago
