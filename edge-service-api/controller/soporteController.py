from utils.db import db
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
        return s.id_ticket
    return {"error": "Cliente not exist. "}


def post_soporte_by_ticket(mensaje, fecha, ticket_id, id_user):
    soporte = Ticket.query.filter(Ticket.id_ticket == ticket_id, Ticket.id_cliente==id_user).one_or_none()
    if soporte:
        s = Mensaje(mensaje, fecha, id_user, ticket_id)
        db.session.add(s)
        db.session.commit()
        return MensajeSchema().dump(s)
    else:
        return 0


def get_soporte_ticket_id(id_user, ticket_id):
    i = Ticket.query.filter(Ticket.id_ticket == ticket_id, Ticket.id_cliente == id_user).one_or_none()

    if i:
        soporte_dict = TicketSchema().dump(i)
        soporte_dict["Mensajes"] = MensajeSchema(many=True).dump(i.mensajes)
        return soporte_dict
    return 0


def get_soporte_user_id(user_id):
    s = Cliente.query.filter(Cliente.id_cliente == user_id).one_or_none()
    if s:
        soporte_dict = ClienteSchema().dump(s)
        soporte_dict["Tickets"] = TicketSchema(many=True).dump(s.ticket)
        return soporte_dict
    return 0


def delete_soporte_ticket_id(id_user, ticket_id):
    s = Ticket.query.filter(Ticket.id_ticket == ticket_id, Ticket.id_cliente == id_user).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        return True
    return False


def delete_message_by_user(id_cliente, id_ticket, msg_id):
    s = Mensaje.query.filter(Mensaje.id_mensaje == msg_id, Mensaje.id_usuari == id_cliente, Mensaje.id_ticket == id_ticket).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        return True
    return False