from models.soporte import Soporte, SoporteSchema
#  from models.chat import Chat, ChatSchema
from utils.db import db


def get_all_soporte():
    i = Soporte.query.all()
    return SoporteSchema(many=True).dump(i)


def post_soporte(descripcion, fecha, estado):
    s = Soporte(descripcion, fecha, estado)
    db.session.add(s)
    db.session.commit()
    return s.ticket_id


def get_soporte_ticket_id_user_id(user_id):
    s = Soporte.query.filter(Soporte.user_id == user_id).one_or_none()
    # if s:
    #     soporte_dict = SoporteSchema().dump(s)

    #     soporte_dict["Chat"] = []
    #     for chat in s.chats:
    #         soporte_dict["Chat"].append(ChatSchema().dump(chat))
    return SoporteSchema(many=True).dump(s)


def post_soporte_user_id(mensaje, fecha, estado):
    s = Soporte(mensaje, fecha, estado)
    db.session.add(s)
    db.session.commit()
    return SoporteSchema.dump(s)


def get_soporte_ticket_id(ticket_id):
    i = Soporte.query.filter(Soporte.ticket_id == ticket_id).one_or_none()
    return SoporteSchema().dump(i)
    # if s:
    #     soporte_dict = SoporteSchema().dump(s)

    #     soporte_dict["Chat"] = []
    #     for chat in s.chats:
    #         soporte_dict["Chat"].append(ChatSchema().dump(chat))


def delete_soporte_ticket_id(ticket_id):
    s = Soporte.query.filter(Soporte.ticket_id == ticket_id).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        return True
    return False
