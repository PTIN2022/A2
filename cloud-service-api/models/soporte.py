from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.chat import Chat  # noqa: F401


class Soporte(db.Model):
    ticket_id = db.Column(db.Integer, nullable=False, primary_key=True)
    # user_id = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Boolean, nullable=False)
    chat = db.relationship("Chat", backref="soporte")

    def __init__(self, descripcion, fecha, estado):
        # self.user_id = user_id
        self.descripcion = descripcion
        self.fecha = fecha
        self.estado = estado


class SoporteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Soporte
        include_fk = True
