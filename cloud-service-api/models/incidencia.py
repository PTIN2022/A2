from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Incidencia(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_estacion = db.Column(db.String(20), nullable=False)  # TODO: foreing key
    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    descripcion = db.Column(db.String(200))

    def __init__(self, id_estacion, fecha, estado, descripcion):
        self.descripcion = descripcion
        self.estado = estado
        self.fecha = fecha
        self.id_estacion = id_estacion


class IncidenciaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incidencia
