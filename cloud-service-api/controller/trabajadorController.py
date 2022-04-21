from models.trabajador import Trabajador, trabajador_schema
from utils.db import db

def post_trabajador(DNI, name, lastname, telf, email, rol, last_access, picture):
	t = Trabajador(DNI, name, lastname, telf, email, rol, int(last_access), picture)
	db.session.add(t)
	db.session.commit()
	
	return trabajador_schema.dumps(t)
