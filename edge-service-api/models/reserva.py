from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Reserva(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_estacion = db.Column(db.String(20), nullable=False)  # TODO: foreing key
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    matricula = db.Column(db.String(7), nullable=False)  # TODO: foreing key
    DNI = db.Column(db.String(9), nullable=False)  # TODO: foreing key
    plaza_id = db.Column(db.Integer, db.ForeignKey("plaza.id"), nullable=False)

    def __init__(self, id_estacion, matricula, fecha_inicio, fecha_fin, DNI, id_plaza):
        self.fecha_fin = fecha_fin
        self.fecha_inicio = fecha_inicio
        self.matricula = matricula
        self.DNI = DNI
        self.id_estacion = id_estacion
        self.plaza_id = id_plaza


class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reserva
        include_fk=True