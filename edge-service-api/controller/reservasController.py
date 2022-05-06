from models.estacion import Estacion
from utils.db import db
from models.reserva import Reserva, ReservaSchema
from models.estacion import Estacion, EstacionSchema
from models.plaza import Plaza, PlazaSchema
from datetime import datetime
import paho.mqtt.publish as publish

def get_all_reservas():
    i = Reserva.query.all()
    return ReservaSchema(many=True).dump(i)


def get_reservas_id(id):
    i = Reserva.query.filter(Reserva.id == id).one_or_none()
    return ReservaSchema().dump(i)


def get_reservas_estacion(estacion):
    # TODO: pillar todos los cargadores de la estacion
    i = Estacion.query.filter(Estacion.estacion == estacion).one_or_none()
    pl_list=[]
    if i:
        dia=datetime.today().strftime('%Y-%m-%d')
        pl_list=[]
        for plaza in i.plazas:
            pl=PlazaSchema().dump(plaza)
            pl["reserva"]=[]
            for reserva in plaza.reservas:
                reserva=ReservaSchema().dump(reserva)
                if reserva["data"] == dia:
                    pl["reserva"].append(reserva)
            pl_list.append(pl)
        return pl_list
    return None
    # TODO: enviar json con horas ocupadas apartir de ahora, 

def get_reservas_matricula(matricula):
    i = Reserva.query.filter(Reserva.matricula == matricula)
    return ReservaSchema(many=True).dump(i)


def get_reservas_dni(dni):
    i = Reserva.query.filter(Reserva.DNI == dni)
    return ReservaSchema(many=True).dump(i)


def post_reserva(id_estacion, matricula, fecha_inicio_str, fecha_final_str, DNI):
    i = Estacion.query.filter(Estacion.estacion == id_estacion).one_or_none()
    plaza_encontrada=False
    if i:
        for plaza in i.plazas:
            if not plaza_encontrada:
                plaza_ocupada=False
                for reserva in plaza.reservas:
                    if not plaza_ocupada:
                        reserva=ReservaSchema().dump(reserva)
                        print("hola")
                        print(reserva)
                        reserva_inicio_data=datetime.strptime(reserva["fecha_inicio"], '%Y-%m-%dT%H:%M:%S')
                        reserva_final_data=datetime.strptime(reserva["fecha_fin"], '%Y-%m-%dT%H:%M:%S')
                        if reserva_inicio_data <= fecha_inicio_str < reserva_final_data or reserva_inicio_data < fecha_final_str <= reserva_final_data:
                            # Comprobando que las fechas que recibimos no este en una reserva
                            if fecha_inicio_str <= reserva_inicio_data < fecha_final_str and fecha_inicio_str < reserva_final_data <= fecha_final_str:
                                # Comprobamos que no haya reservas en la franja horaria de la reserva solicitante
                                plaza_ocupada=True
                if not plaza_ocupada:
                    pl=PlazaSchema().dump(plaza)
                    i = Reserva(id_estacion, matricula, fecha_inicio_str, fecha_final_str, DNI, pl["id"])
                    db.session.add(i)
                    db.session.commit()
                    print(ReservaSchema().dump(i))
                    publish.single("estacion/"+str(id_estacion)+"/cargador/"+str(pl["id"])+"/reserva", str(ReservaSchema().dump(i)), hostname="test.mosquitto.org", port=1883)
                    plaza_encontrada=True
                    return i.id
    if not plaza_encontrada:
        return None


def remove_reserva(id):
    i = Reserva.query.filter(Reserva.id == id).one_or_none()
    if i:
        db.session.delete(i)
        db.session.commit()
        return True
    return False


def modify_reserva(id, id_estacion=None, desde=None, hasta=None, matricula=None, data=None, DNI=None):
    i = Reserva.query.filter(Reserva.id == id).one_or_none()
    if i:
        if id_estacion:
            i.id_estacion = id_estacion
        if desde:
            i.desde = desde
        if hasta:
            i.hasta = hasta
        if matricula:
            i.matricula = matricula
        if data:
            i.data = data
        if DNI:
            i.DNI = DNI

        db.session.commit()
        return ReservaSchema().dump(i)

    return None
