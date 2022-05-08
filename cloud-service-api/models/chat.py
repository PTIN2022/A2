from utils.db import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Chat(db.Model):
    msg_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("soporte.user_id"), nullable=False)
    mensaje = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.String(15), nullable=False)

    def __init__(self, user_id, mensaje, fecha):
        self.user_id = user_id
        self.mensaje = mensaje
        self.fecha = fecha


class ChatSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Chat
