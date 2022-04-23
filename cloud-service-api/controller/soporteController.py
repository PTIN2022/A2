from models.soporte import Soporte, soporte_schema
from utils.db import db

def get_soporte_ticket_id(ticket_id):
    s = Soporte.query.filter(Soporte.ticket_id == ticket_id).one_or_none()
    return s.to_dict()

def post_soporte(user_id, ticket_id, fecha, descripcion):
    s = Soporte(user_id, ticket_id, fecha, descripcion)
    db.session.add(s)
    db.session.commit()
    return s.to_dict()
    
def post_soporte_ticket_id_user_id(user_id):
    s = Soporte(user_id)
    db.session.add(s)
    db.session.commit()
    return s.to_dict()

def delete_soporte_ticket_id(ticket_id):
    s = Soporte.query.filter(Soporte.ticket_id == ticket_id).one_or_none()
    if s:
        db.session.delete(s)
        db.session.commit()
        return True
    return False
