from utils.db import db
from models.vehiculo import Vehiculo
from models.cliente import Cliente
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class VehiculoCliente(db.Model):
    id_vehiculo = db.Column('id_vehiculo', db.ForeignKey('vehiculo.id_vehiculo'), nullable=False)
    id_cliente = db.Column('id_cliente', db.ForeignKey('cliente.id_usuari'), nullable=False)
    __table_args__ = (
        db.PrimaryKeyConstraint(id_vehiculo, id_cliente),
        {},
    )

    def __init__(self, id_vehiculo, id_cliente):
        self.id_vehiculo = id_vehiculo
        self.id_cliente = id_cliente


class VehiculoClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = VehiculoCliente
