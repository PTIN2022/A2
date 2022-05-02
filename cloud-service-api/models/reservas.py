from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Reserva(db.Model):

    id_reserva = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    estacion = db.Column(db.String(20), nullable=False)
    desde = db.Column(db.String(5), nullable=False)
    hasta = db.Column(db.String(5), nullable=False)
    matricula = db.Column(db.String(7), nullable=False)
    fecha = db.Column(db.String(10), nullable=False)
    DNI = db.Column(db.String(9), nullable=False)

    def __init__(self, estacion, desde, hasta, matricula, fecha, DNI):
        self.desde = desde
        self.hasta = hasta
        self.matricula = matricula
        self.fecha = fecha
        self.DNI = DNI
        self.estacion = estacion


class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
