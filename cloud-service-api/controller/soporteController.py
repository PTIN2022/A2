from utils.db import db
from utils.mqtt_utils import send_to_edge
from models.model import ClienteSchema, Ticket, TicketSchema, Mensaje, MensajeSchema, Cliente


def get_all_soporte():
    i = Ticket.query.all()
    return TicketSchema(many=True).dump(i)


def post_soporte(descripcion, fecha, id_cliente, asunto):
    c = Cliente.query.filter(Cliente.id_cliente == id_cliente).one_or_none()
    if c:
        s = Ticket(fecha, asunto, descripcion, "Pendiente", c.id_cliente)
        db.session.add(s)
        db.session.commit()
        send_to_edge("gesys/edge/soporte/add", TicketSchema().dump(s))
        return s.id_ticket
    return None


def get_soporte_user_id(user_id):
    s = Cliente.query.filter(Cliente.dni == user_id).one_or_none()
    print(s)
    print(s.ticket)
    if s:
        soporte_dict = ClienteSchema().dump(s)
        soporte_dict["Tickets"] = TicketSchema(many=True).dump(s.ticket)
        return soporte_dict
    return None


def post_soporte_by_ticket(mensaje, fecha, ticket_id, id_user):
    soporte = Ticket.query.filter(Ticket.id_ticket == ticket_id).one_or_none()
    if soporte:
        s = Mensaje(mensaje, fecha, id_user, ticket_id)
        db.session.add(s)
        db.session.commit()
        send_to_edge("gesys/edge/soporte/response", MensajeSchema().dump(s))
        return MensajeSchema().dump(s)
    else:
        return None


def put_soporte_by_ticket(ticket_id, estado=None):
    soporte = Ticket.query.filter(Ticket.id_ticket == ticket_id).one_or_none()
    if soporte:
        if estado:
            soporte.estado = estado
            send_to_edge("gesys/edge/soporte/status", {"estado": estado, "id_ticket": ticket_id})
        db.session.commit()
        return TicketSchema().dump(soporte)
    else:
        return None


def get_soporte_ticket_id(ticket_id):
    i = Ticket.query.filter(Ticket.id_ticket == ticket_id).one_or_none()

    if i:
        soporte_dict = TicketSchema().dump(i)
        soporte_dict["Mensajes"] = MensajeSchema(many=True).dump(i.mensajes)
        return soporte_dict
    return None


def delete_soporte_ticket_id(ticket_id):
    s = Ticket.query.filter(Ticket.id_ticket == ticket_id).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        send_to_edge("gesys/edge/soporte/remove", {"ticket_id": ticket_id})
        return True
    return False


def delete_message_by_user(msg_id):
    s = Mensaje.query.filter(Mensaje.id_mensaje == msg_id).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        send_to_edge("gesys/edge/soporte/message/remove", {"msg_id": msg_id})
        return True
    return False
