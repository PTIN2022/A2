from models.soporte import Soporte, SoporteSchema
from models.chat import Chat, ChatSchema
from utils.db import db


def get_all_soporte():
    i = Soporte.query.all()
    return SoporteSchema(many=True).dump(i)


def post_soporte(fecha, descripcion):
    s = Soporte(fecha, descripcion)
    db.session.add(s)
    db.session.commit()
    return s.to_dict()


def get_soporte_ticket_id_user_id(user_id):

    s = Soporte.query.filter(Soporte.user_id == user_id).one_or_none()
    if s:
        soporte_dict = SoporteSchema().dump(s)

        soporte_dict["Chat"] = []
        for chat in s.chats:
            soporte_dict["Chat"].append(ChatSchema().dump(chat))

    return s.to_dict()


def post_soporte_user_id(mensaje, fecha):
    s = Soporte(mensaje, fecha)
    db.session.add(s)
    db.session.commit()
    return s.to_dict()


def get_soporte_ticket_id(ticket_id):

    s = Soporte.query.filter(Soporte.ticket_id == ticket_id).one_or_none()
    if s:
        soporte_dict = SoporteSchema().dump(s)

        soporte_dict["Chat"] = []
        for chat in s.chats:
            soporte_dict["Chat"].append(ChatSchema().dump(chat))

    return s.to_dict()


def delete_soporte_ticket_id(ticket_id):
    s = Soporte.query.filter(Soporte.ticket_id == ticket_id).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        return True
    return False
