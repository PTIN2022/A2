from models.trabajador import Trabajador, trabajador_schema
from utils.db import db

trabajadores_list = [
  {
	"dni": "60748880S",
	"name": "Pere",
	"lastname": "Roca",
	"telf": "622554433",
	"email": "pere.roca@boss.com",
	"rol": "dueño",
	"last_access": -1,
	"picture": "http://?????????/trabajadores/PereRoca.png"
  },
  {
	"dni": "40748880S",
	"name": "Guillem",
	"lastname": "Guzman",
	"telf": "622554433",
	"email": "guillem.guzman@boss.com",
	"rol": "programmer",
	"last_access": -1,
	"picture": "http://?????????/trabajadores/guillem.png"
  }
]

def post_trabajador(DNI, name, lastname, telf, email, rol, last_access, picture):
    t = Trabajador(DNI, name, lastname, telf, email, rol, int(last_access), picture)
    db.session.add(t)
    db.session.commit()
    
    return t.to_dict()

def get_all_trabajadores():
    t = Trabajador.query.all()
    return trabajador_schema.dumps(t)
    
def get_trabajador_dni(dni):
    for trabajador in trabajadores_list:
        if trabajador["dni"] == str(dni):
            return trabajador
    return None

# habra que mojararlo (last_access, picture...)
def modify_trabajador(DNI, name=None, lastname=None, telf=None, email=None, rol=None, last_access=None, picture=None):
    for index in range(len(trabajadores_list)):
        if "dni" in trabajadores_list[index]:
            if DNI == trabajadores_list[index]["dni"]:
                trabajador_orig = trabajadores_list[index]
                if (name):
                    trabajador_orig["name"] = name 
                if (lastname):
                    trabajador_orig["lastname"] = direccion
                if (telf):
                    trabajador_orig["telf"] = telf
                if (email):
                    trabajador_orig["email"] = email
                if (rol):
                    trabajador_orig["rol"] = rol
                if (last_access):
                    trabajador_orig["last_access"] = last_access
                if (picture):
                    trabajador_orig["picture"] = picture

                trabajadores_list[index] =  trabajador_orig
                return trabajador_orig

    return None

def delete_trabajador(dni):
    for trabajador in trabajadores_list:
        print(trabajador["dni"], str(dni))
        if trabajador["dni"] == str(dni):
            trabajadores_list.remove(trabajador)
            return True

    return False
