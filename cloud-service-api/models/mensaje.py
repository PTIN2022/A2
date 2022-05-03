from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Mensaje(db.Model):
    mensaje_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey("soporte.ticket_id"), nullable=False)
    contenido = db.Column(db.String(500), nullable=False)

    def __init__(self, user_id, ticket_id, contenido):
        self.user_id = user_id
        self.ticket_id = contenido
        self.contenido = contenido

    def to_dict(self):
        return {"ticket_id": self.ticket_id, "user_id": self.user_id, "descripcion": self.contenido}


class MensajeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mensaje


Mensaje_schema = MensajeSchema(many=True)
