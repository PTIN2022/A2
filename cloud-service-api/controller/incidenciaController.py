from models.incidencia import Incidencia, incidencia_schema
from utils.db import db


incidencias_list = [
  {
    "incidenciaId": 1,
    "estacion": "VG1",
    "direccion": "Av.Victor Balaguer 2",
    "fecha_averia": "18/04/2022",
    "estado": False,
    "descripcion": "El cargador de la planta 2 m plaza 1 no funciona"
  },
  {
    "incidenciaId": 2,
    "estacion": "VG2",
    "direccion": "Av.Victor Balaguer 2",
    "fecha_averia": "18/04/2022 ",
    "estado": False,
    "descripcion": "El cargador de la planta 2 m plaza 1 no funciona"
  }
]


def get_all_incidencias():
    i = Incidencia.query.all()
    return incidencia_schema.dumps(i)


def get_incidencias_id(id):
    for incidencia in incidencias_list:
        if "incidenciaId" in incidencia:
            if incidencia["incidenciaId"] == int(id):
                return incidencia
    return None


def get_incidencias_estacion(estacion):
    for incidencia in incidencias_list:
        if "estacion" in incidencia:
            if incidencia["estacion"] == estacion:
                return incidencia
    return None


# post_incidencia(1, "qwe", "qwer", "8/23", "desc")
def post_incidencia(estacion, direccion, fecha, descripcion, estado=False):

    print(fecha)
    print(type(fecha))
    i = Incidencia(estacion, fecha, estado, descripcion)

    db.session.add(i)
    db.session.commit()

    return 1


def remove_incidencia():
    for incidencia in incidencias_list:
        if "incidenciaId" in incidencia:
            if incidencia["incidenciaId"] == int(id):
                incidencias_list.remove(incidencia)
    return None


def modify_incidencia(id, estacion=None, direccion=None, fecha_averia=None, descripcion=None, estado=None):
    print(estado)
    for index in range(len(incidencias_list)):
        if "incidenciaId" in incidencias_list[index]:
            if int(id) == incidencias_list[index]["incidenciaId"]:
                incidencia_orig = incidencias_list[index]
                if (estacion):
                    incidencia_orig["estacion"] = estacion
                if (direccion):
                    incidencia_orig["direccion"] = direccion
                if (fecha_averia):
                    incidencia_orig["fecha_averia"] = fecha_averia
                if (descripcion):
                    incidencia_orig["descripcion"] = descripcion
                if (estado is not None):
                    incidencia_orig["estado"] = estado

                incidencias_list[index] = incidencia_orig
                return incidencia_orig

    return None


def deleted_incidencias(id):
    for incidencia in incidencias_list:
        if "incidenciaId" in incidencia:
            incidencias_list.remove(incidencia)
            return True

    return False
