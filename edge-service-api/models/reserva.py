from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Reserva(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_estacion = db.Column(db.String(20), nullable=False)  # TODO: foreing key
    desde = db.Column(db.String(5), nullable=False)
    hasta = db.Column(db.String(5), nullable=False)
    matricula = db.Column(db.String(7), nullable=False) # TODO: foreing key
    data = db.Column(db.String(10), nullable=False)
    DNI = db.Column(db.String(9), nullable=False) # TODO: foreing key

    def __init__(self, id_estacion, desde, hasta, matricula, data, DNI):
        self.desde = desde
        self.hasta = hasta
        self.matricula = matricula
        self.data = data
        self.DNI = DNI
        self.id_estacion = id_estacion


class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
