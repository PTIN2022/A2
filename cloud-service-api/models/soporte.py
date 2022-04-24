from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Soporte(db.Model):
    ticket_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.String(15), nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    mensaje = db.Column(db.String(200), nullable=False)

    def __init__(self, ticket_id, user_id, descripcion, fecha, email, rol, estado, mensaje):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.descripcion = descripcion
        self.fecha = fecha
        self.estado = estado
        self.mensaje = mensaje

    def to_dict(self):
        return {"ticket_id": self.ticket_id, "user_id": self.user_id, "descripcion": self.descripcion, "fecha": self.fecha, "estado": self.estado, "mensaje": self.mensaje}


class SoporteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Soporte


soporte_schema = SoporteSchema(many=True)
