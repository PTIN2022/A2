from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Chat(db.Model):
    msg_id = db.Column(db.Integer, nullable=False, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey("Cliente.id_cliente"), nullable=False)
    mensaje = db.Column(db.Integer, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey("soporte.ticket_id"), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)

    def __init__(self, ticket_id, mensaje, fecha):
        self.ticket_id = ticket_id
        self.mensaje = mensaje
        self.fecha = fecha


class ChatSchema(SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Chat
